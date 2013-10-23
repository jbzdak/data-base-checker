# -*- coding: utf-8 -*-
from collections.abc import Sequence
import difflib
import pprint
import unittest
from unittest.util import safe_repr


def make_tc():
    btc =  BetterTestCase()
    btc.longMessage = True
    btc.maxDiff = 1024 * 1024
    return btc

class BetterTestCase(unittest.TestCase):
    """
    Basically because of http://bugs.python.org/issue19217 we can't compare
    errorneus student's submissions. This subclass contains code from
    patch attached there so whole thing works.

    When this bug is merged replace this with normal TestCase.
    """

    def assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None):
        """An equality assertion for ordered sequences (like lists and tuples).

        For the purposes of this function, a valid ordered sequence type is one
        which can be indexed, has a length, and has an equality operator.

        Args:
            seq1: The first sequence to compare.
            seq2: The second sequence to compare.
            seq_type: The expected datatype of the sequences, or None if no
                    datatype should be enforced.
            msg: Optional message to use on failure instead of a list of
                    differences.
        """
        if seq_type is not None:
            seq_type_name = seq_type.__name__
            if not isinstance(seq1, seq_type):
                raise self.failureException('First sequence is not a %s: %s'
                                        % (seq_type_name, safe_repr(seq1)))
            if not isinstance(seq2, seq_type):
                raise self.failureException('Second sequence is not a %s: %s'
                                        % (seq_type_name, safe_repr(seq2)))
        else:
            seq_type_name = "sequence"

        max_seq_len = 0
        differing = None
        try:
            len1 = max_seq_len = len(seq1)
        except (TypeError, NotImplementedError):
            differing = 'First %s has no length.    Non-sequence?' % (
                    seq_type_name)

        if differing is None:
            try:
                len2 = len(seq2)
            except (TypeError, NotImplementedError):
                differing = 'Second %s has no length.    Non-sequence?' % (
                        seq_type_name)
            else:
                if len2 > max_seq_len:
                    max_seq_len = len2


        if differing is None:
            if seq1 == seq2:
                return

            seq1_repr = safe_repr(seq1)
            seq2_repr = safe_repr(seq2)
            if len(seq1_repr) > 30:
                seq1_repr = seq1_repr[:30] + '...'
            if len(seq2_repr) > 30:
                seq2_repr = seq2_repr[:30] + '...'
            elements = (seq_type_name.capitalize(), seq1_repr, seq2_repr)
            differing = '%ss differ: %s != %s\n' % elements

            for i in range(min(len1, len2)):
                try:
                    item1 = seq1[i]
                except (TypeError, IndexError, NotImplementedError):
                    differing += ('\nUnable to index element %d of first %s\n' %
                                 (i, seq_type_name))
                    break

                try:
                    item2 = seq2[i]
                except (TypeError, IndexError, NotImplementedError):
                    differing += ('\nUnable to index element %d of second %s\n' %
                                 (i, seq_type_name))
                    break

                if item1 != item2:
                    differing += ('\nFirst differing element %d:\n%s\n%s\n' %
                                 (i, item1, item2))
                    break
            else:
                if (len1 == len2 and seq_type is None and
                    type(seq1) != type(seq2)):
                    # The sequences are the same, but have differing types.
                    return

            if len1 > len2:
                differing += ('\nFirst %s contains %d additional '
                             'elements.\n' % (seq_type_name, len1 - len2))
                try:
                    differing += ('First extra element %d:\n%s\n' %
                                  (len2, seq1[len2]))
                except (TypeError, IndexError, NotImplementedError):
                    differing += ('Unable to index element %d '
                                  'of first %s\n' % (len2, seq_type_name))
            elif len1 < len2:
                differing += ('\nSecond %s contains %d additional '
                             'elements.\n' % (seq_type_name, len2 - len1))
                try:
                    differing += ('First extra element %d:\n%s\n' %
                                  (len1, seq2[len1]))
                except (TypeError, IndexError, NotImplementedError):
                    differing += ('Unable to index element %d '
                                  'of second %s\n' % (len1, seq_type_name))
        standardMsg = differing
        # calculating the diff might take a long time and produce unreadable
        # output if there are too many elements
        if max_seq_len < 30:
            diffMsg = '\n' + '\n'.join(
                difflib.ndiff(pprint.pformat(seq1).splitlines(),
                              pprint.pformat(seq2).splitlines()))
            standardMsg = self._truncateMessage(standardMsg, diffMsg)

        msg = self._formatMessage(msg, standardMsg)
        self.fail(msg)