from __future__ import division
import itertools
import math
import unicodedata
import re
import stringprep

from django.core.exceptions import ValidationError
from django.utils.encoding import smart_text
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from password_policies.conf import settings

try:
    # Python 3 does not have an xrange, this will throw a NameError
    xrange
except NameError:
    pass
else:
    # alias range to xrange for Python 2
    range = xrange


class BaseCountValidator(object):
    """
Counts the occurrences of characters of a
:py:func:`unicodedata.category` and raises a
:class:`~django.core.exceptions.ValidationError` if the count
is less than :py:func:`~BaseCountValidator.get_min_count`.
"""
    def __call__(self, value):
        if not self.get_min_count():
            return
        counter = 0
        for character in force_text(value):
            category = unicodedata.category(character)
            if category in self.categories:
                counter += 1
        if counter < self.get_min_count():
            raise ValidationError(self.get_error_message(), code=self.code)

    def get_error_message(self):
        """Returns the error message of this validator."""
        raise NotImplementedError

    def get_min_count(self):
        """Returns the amount of required characters."""
        raise NotImplementedError


class BaseRFC4013Validator(object):
    """
Validates that a given password passes the requirements as
defined in `RFC 4013`_.

.. _`RFC 4013`: http://tools.ietf.org/html/rfc4013
"""
    first = u''
    invalid = True
    l_cat = False
    last = u''
    r_and_al_cat = False

    def __call__(self, value):
        value = force_text(value)
        self.first = value[0]
        self.last = value[:-1]
        self._process(value)

    def _process(self, value):
        for code in force_text(value):
            # TODO: Is this long enough?
            if stringprep.in_table_c12(code) or stringprep.in_table_c21_c22(code) or \
                stringprep.in_table_c3(code) or stringprep.in_table_c4(code) or \
                stringprep.in_table_c5(code) or stringprep.in_table_c6(code) or \
                stringprep.in_table_c7(code) or stringprep.in_table_c8(code) or \
                    stringprep.in_table_c9(code):
                self.invalid = False
            if stringprep.in_table_d1(code):
                self.r_and_al_cat = True
            if stringprep.in_table_d2(code):
                self.l_cat = True


class BaseSimilarityValidator(object):
    """
Compares a `needle` to a `haystack` (list of strings) and calculates
a similarity between 0.0 and 1.0.

Raises a :class:`~django.core.exceptions.ValidationError` if the similarity
is greater than :py:attr:`~password_policies.conf.Settings.PASSWORD_MATCH_THRESHOLD`.
"""
    # Taken from django-passwords

    #: A list of strings.
    haystacks = []

    def __init__(self, haystacks=[]):
        if haystacks:
            self.haystacks = haystacks

    def __call__(self, value):
        needle = force_text(value)
        for haystack in self.haystacks:
            distance = self.fuzzy_substring(needle, haystack)
            longest = max(len(needle), len(haystack))
            similarity = (longest - distance) / longest
            if similarity >= self.get_threshold():
                raise ValidationError(
                    self.message % {"haystacks": ", ".join(self.haystacks)},
                    code=self.code)

    def fuzzy_substring(self, needle, haystack):
        needle, haystack = needle.lower(), haystack.lower()
        m, n = len(needle), len(haystack)

        if m == 1:
            if needle not in haystack:
                return -1
        if not n:
            return m

        row1 = [0] * (n + 1)
        for i in range(0, m):
            row2 = [i + 1]
            for j in range(0, n):
                cost = (needle[i] != haystack[j])
                row2.append(min(row1[j + 1] + 1, row2[j] + 1, row1[j] + cost))
            row1 = row2
        return min(row1)

    def get_threshold(self):
        """
:returns: :py:attr:`password_policies.conf.Settings.PASSWORD_MATCH_THRESHOLD`.
"""
        return settings.PASSWORD_MATCH_THRESHOLD


class BidirectionalValidator(BaseRFC4013Validator):
    """
Validates that

* a string containing any RandALCat character does not contain any
  LCat character.
* a string containing any RandALCat character does start and end
  with a RandALCat character.

For more information read `RFC 4013, section 2.3`_.

.. _`RFC 4013, section 2.3`: http://tools.ietf.org/html/rfc4013#section-2.3
"""
    #: The validator's error code.
    code = u"invalid_bidirectional"
    #: The validator's error message.
    message = _("The new password contains ambiguous bidirectional characters.")

    def __call__(self, value):
        super(BidirectionalValidator, self).__call__(value)
        if self.r_and_al_cat:
            if self.l_cat or not stringprep.in_table_d1(self.first) or not stringprep.in_table_d1(self.last):
                raise ValidationError(self.message, code=self.code)


class CommonSequenceValidator(BaseSimilarityValidator):
    """
Validates that a given password is not based on a common sequence of characters.
"""
    # Taken from django-passwords

    #: The validator's error code.
    code = u"invalid_common_sequence"
    #: The validator's error message.
    message = _("The new password is based on a common sequence of characters.")


class ConsecutiveCountValidator(object):
    """
Validates that a given password does not contain consecutive characters.
"""
    #: The validator's error code.
    code = u"invalid_consecutive_count"

    def __call__(self, value):
        if not self.get_max_count():
            return
        consecutive_found = False
        for _, group in itertools.groupby(force_text(value)):
            if len(list(group)) > self.get_max_count():
                consecutive_found = True
        if consecutive_found:
            msg = ungettext("The new password contains consecutive"
                            " characters. Only %(count)d consecutive character"
                            " is allowed.",
                            "The new password contains consecutive"
                            " characters. Only %(count)d consecutive characters"
                            " are allowed.",
                            self.get_max_count()) % {'count': self.get_max_count()}
            raise ValidationError(msg, code=self.code)

    def get_max_count(self):
        """
:returns: :py:attr:`password_policies.conf.Settings.PASSWORD_MAX_CONSECUTIVE`
"""
        return settings.PASSWORD_MAX_CONSECUTIVE


class CracklibValidator(object):
    """
Validates a given password using Python bindings for cracklib.
"""
    #: The validator's error code.
    code = u"invalid_cracklib"
    #: This argument will change the default of 10 for the number
    #: of characters in the new password that must not be present
    #: in the old password. In addition, if 1/2 of the characters
    #: in the new password are different then the new password will
    #: be accepted anyway.
    diff_ok = 0
    #: The maximum credit for having digits in the new
    #: password.
    dig_credit = 0
    #: The maximum credit for having lower case letters in
    #: the new password.
    low_credit = 0
    #: The minimum acceptable size for the new password (plus one
    #: if credits are not disabled which is the default).
    min_length = 6
    #: The maximum credit for having other characters in the new
    #: password.
    oth_credit = 0
    #: The maximum credit for having upper case letters in the
    #: new password.
    up_credit = 0

    def __call__(self, value):
        if not settings.PASSWORD_USE_CRACKLIB:
            return
        try:
            import crack
        except ImportError:
            return
        crack.diff_ok = self.diff_ok
        crack.dig_credit = self.dig_credit
        crack.low_credit = self.low_credit
        crack.min_length = self.min_length
        crack.oth_credit = self.oth_credit
        crack.up_credit = self.up_credit
        try:
            crack.FascistCheck(value)
        except ValueError as reason:
            reason = _(str(reason))
            message = _("Please choose a different password, %s." % reason)
            raise ValidationError(message, code=self.code)

    def __init__(self, diff_ok=0, dig_credit=0, low_credit=0,
                 min_length=0, oth_credit=0, up_credit=0):
        self.diff_ok = diff_ok
        self.dig_credit = dig_credit
        self.low_credit = low_credit
        self.min_length = min_length
        self.oth_credit = oth_credit
        self.up_credit = up_credit


class EntropyValidator(object):
    """
Validates that a password contains varied characters by calculating
the Shannon entropy of a password.
"""
    # Taken from revelation

    #: The validator's error code.
    code = u"invalid_entropy"
    #: Specifies the minimum entropy of long passwords
    #: (len(password) >= 100). Defaults to
    #: :py:attr:`password_policies.conf.Settings.PASSWORD_MIN_ENTROPY_LONG`.
    #:
    #: If set to 0 validation will not be performed.
    long_min_entropy = settings.PASSWORD_MIN_ENTROPY_LONG
    #: The validator's error message.
    message = _("The new password is not varied enough.")
    #: Specifies the minimum entropy of short passwords
    #: (len(password) < 100). Defaults to
    #: :py:attr:`password_policies.conf.Settings.PASSWORD_MIN_ENTROPY_SHORT`.
    #:
    #: If set to 0 validation will not be performed.
    short_min_entropy = settings.PASSWORD_MIN_ENTROPY_SHORT

    def __call__(self, value):
        pwlen = len(value)
        if pwlen < 100 and not self.short_min_entropy:
            return
        else:
            if not self.long_min_entropy:
                return
        ent = self.entropy(value)
        idealent = self.entropy_ideal(pwlen)
        try:
            ent_quotient = ent / idealent
        except ZeroDivisionError:
            ent_quotient = 0
        if (pwlen < 100 and ent_quotient < self.short_min_entropy) or (pwlen >= 100 and ent < self.long_min_entropy):
            raise ValidationError(self.message, code=self.code)

    def entropy(self, string):
        # Calculates the Shannon entropy of a string
        #
        # get probability of chars in string
        prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
        # calculate the entropy
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
        return entropy

    def entropy_ideal(self, length):
        # Calculates the ideal Shannon entropy of a string with given length
        prob = 1.0 / length
        return -1.0 * length * prob * math.log(prob) / math.log(2.0)


class DictionaryValidator(BaseSimilarityValidator):
    """
Validates that a given password is not based on a dictionary word.

.. note::
    If :py:attr:`~DictionaryValidator.dictionary`
    AND :py:attr:`~DictionaryValidator.words` are empty or set
    to None validation is not performed.

.. warning::
    This validator is very time consuming and validation
    duration depends on the amount of lines in the dictionary
    file. The larger the dictionary file, the longer validation
    takes!
"""
    # Taken from django-passwords

    #: The validator's error code.
    code = u"invalid_dictionary_word"
    #: A path to a file with one word per line. Defaults to
    #: :py:attr:`password_policies.conf.Settings.PASSWORD_DICTIONARY`.
    dictionary = ''
    #: The validator's error message.
    message = _("The new password is based on a dictionary word.")
    #: A list of unicode strings. Defaults to
    #: :py:attr:`password_policies.conf.Settings.PASSWORD_WORDS`.
    words = []

    def __init__(self, dictionary='', words=[]):
        if not dictionary:
            self.dictionary = settings.PASSWORD_DICTIONARY
        else:
            self.dictionary = dictionary
        if not words:
            self.words = settings.PASSWORD_WORDS
        else:
            self.words = words
        haystacks = []
        if self.dictionary:
            with open(self.dictionary) as dictionary:
                haystacks.extend(
                    [smart_text(x.strip()) for x in dictionary.readlines()]
                )
        if self.words:
            haystacks.extend(self.words)
        super(DictionaryValidator, self).__init__(haystacks=haystacks)


class InvalidCharacterValidator(BaseRFC4013Validator):
    """
Validates that a given password does not contain invalid unicode
characters as defined in `RFC 4013, section 2.3`_.

.. _`RFC 4013, section 2.3`: http://tools.ietf.org/html/rfc4013#section-2.3
"""
    #: The validator's error code.
    code = u"invalid_unicode"
    #: The validator's error message.
    message = _("The new password contains invalid unicode characters.")

    def __call__(self, value):
        super(InvalidCharacterValidator, self).__call__(value)
        if self.invalid:
            raise ValidationError(self.message, code=self.code)


class LetterCountValidator(BaseCountValidator):
    """
Counts the occurrences of letters and raises a
:class:`~django.core.exceptions.ValidationError` if the count
is less than :func:`~LetterCountValidator.get_min_count`.
"""
    categories = ['LC', 'Ll', 'Lu', 'Lt', 'Lo', 'Nl']
    """
The unicode data letter categories:

====  ===========
Code  Description
====  ===========
LC    Letter, Cased
Ll    Letter, Lowercase
Lu    Letter, Uppercase
Lt    Letter, Titlecase
Lo    Letter, Other
Nl    Number, Letter
====  ===========

"""
    #: The validator's error code.
    code = u"invalid_letter_count"

    def get_error_message(self):
        """
Returns this validator's error message.
"""
        msg = ungettext("The new password must contain %d or more letter.",
                        "The new password must contain %d or more letters.",
                        self.get_min_count()) % self.get_min_count()
        return msg

    def get_min_count(self):
        """
:returns: :py:attr:`password_policies.conf.Settings.PASSWORD_MIN_LETTERS`
"""
        return settings.PASSWORD_MIN_LETTERS


class NotEmailValidator(object):
    """
Validates that a given password is not similar to an email address.
"""
    #: The validator's error code.
    code = u"invalid_email_used"
    #: The validator's error message.
    message = _("The new password is similar to an email address.")
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*$"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"$)',  # quoted-string
        re.IGNORECASE)
    domain_regex = re.compile(
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?$)'  # domain
        # literal form, ipv4 address (SMTP 4.1.3)
        r'|^\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$',
        re.IGNORECASE)

    def __call__(self, value):
        """
Validates that the input does not match the regular expression.
"""
        user_part_found = False
        domain_part_found = False
        if value and '@' in value:
            user_part, domain_part = value.rsplit('@', 1)
            if self.user_regex.match(user_part):
                user_part_found = True
            if not self.domain_regex.match(domain_part):
                # Try for possible IDN domain-part
                try:
                    domain_part = domain_part.encode('idna').decode('ascii')
                    if self.domain_regex.match(domain_part):
                        domain_part_found = True
                except UnicodeError:
                    pass
            else:
                domain_part_found = True
            if user_part_found and domain_part_found:
                raise ValidationError(self.message, code=self.code)


class NumberCountValidator(BaseCountValidator):
    """
Counts the occurrences of numbers (digits, etc.) and raises a
:class:`~django.core.exceptions.ValidationError` if the count
is less than :py:func:`~NumberCountValidator.get_min_count`.
"""
    categories = ['Nd', 'No']
    """
The unicode data number categories:

====  ===========
Code  Description
====  ===========
Nd    Number, Decimal Digit
No    Number, Other
====  ===========

"""
    #: The validator's error code.
    code = u"invalid_number_count"

    def get_error_message(self):
        """
Returns this validator's error message.
"""
        msg = ungettext("The new password must contain %d or more number.",
                        "The new password must contain %d or more numbers.",
                        self.get_min_count()) % self.get_min_count()
        return msg

    def get_min_count(self):
        """
:returns: :py:attr:`password_policies.conf.Settings.PASSWORD_MIN_NUMBERS`
"""
        return settings.PASSWORD_MIN_NUMBERS


class SymbolCountValidator(BaseCountValidator):
    """
Counts the occurrences of other characters than letters and numbers,
except line breaks, and raises a
:class:`~django.core.exceptions.ValidationError` if the count
is less than :py:func:`~SymbolCountValidator.get_min_count`.
"""
    categories = ['Lm', 'Mc', 'Me', 'Mn', 'Pc', 'Pd', 'Pe', 'Pf',
                  'Pi', 'Po', 'Ps', 'Sc', 'Sk', 'Sm', 'So', 'Zl']
    """
The unicode data symbol categories:

====  ===========
Code  Description
====  ===========
Lm    Letter, Modifier
Mc    Mark, Spacing Combining
Me    Mark, Enclosing
Mn    Mark, Nonspacing
Pc    Punctuation, Connector
Pd    Punctuation, Dash
Pe    Punctuation, Close
Pf    Punctuation, Final quote (may behave like Ps or Pe depending on usage)
Pi    Punctuation, Initial quote (may behave like Ps or Pe depending on usage)
Po    Punctuation, Other
Ps    Punctuation, Open
Sc    Symbol, Currency
Sk    Symbol, Modifier
Sm    Symbol, Math
So    Symbol, Other
Zl    Separator, Line
====  ===========

"""
    #: The validator's error code.
    code = u"invalid_symbol_count"

    def get_error_message(self):
        """
Returns this validator's error message.
"""
        msg = ungettext("The new password must contain %d or more symbol.",
                        "The new password must contain %d or more symbols.",
                        self.get_min_count()) % self.get_min_count()
        return msg

    def get_min_count(self):
        """
:returns: :py:attr:`password_policies.conf.Settings.PASSWORD_MIN_SYMBOLS`
"""
        return settings.PASSWORD_MIN_SYMBOLS


validate_bidirectional = BidirectionalValidator()
validate_common_sequences = CommonSequenceValidator(settings.PASSWORD_COMMON_SEQUENCES)
validate_consecutive_count = ConsecutiveCountValidator()
validate_cracklib = CracklibValidator()
validate_dictionary_words = DictionaryValidator(dictionary=settings.PASSWORD_DICTIONARY)
validate_entropy = EntropyValidator()
validate_invalid_character = InvalidCharacterValidator()
validate_letter_count = LetterCountValidator()
validate_not_email = NotEmailValidator()
validate_number_count = NumberCountValidator()
validate_symbol_count = SymbolCountValidator()
