from utils import SequenceManipulations as sm

__author__ = 'ofirr'


class DNA(object):

    def __init__(self,seq):
        if isinstance(seq,str):
            s = seq.upper()
            for i in s:
                if i not in "ACGT":
                    raise ValueError("Invalid DNA base - not one of A,C,T,G.")
            self._seq = s
        else:
            raise TypeError("DNA accepts only string (bytearray) objects.")

    @property
    def seq(self):
        return self._seq

    def rev_comp(self):
        return DNA(sm.complement(self.seq)[::-1])

    def rev(self):
        return DNA(self.seq[::-1])

    def comp(self):
        return DNA(sm.complement(self.seq))

    def __add__(self, other):
        if not isinstance(other,DNA):
            raise TypeError("unsupported operand type(s) for +: '%s' and '%s'"
                            % (type(self), type(other)))
        # Can be optimized to omit ctor check.
        return DNA(self.seq + other.seq)

    def __getitem__(self,num_or_slice):
        if not isinstance(num_or_slice,slice):
            raise ValueError("Only returns slices")
        if num_or_slice.step is not None:
            raise ValueError("No step")
        return DNA(self.seq[num_or_slice])

    def __str__(self):
        return self.seq

    def __unicode__(self):
        return self.seq.decode("ascii")

    def __repr__(self):
        return "DNA(\"%s\")" % (self.seq)

    def __eq__(self, other):
        if not isinstance(other,DNA):
            raise TypeError("unsupported operand type(s) for ==: '%s' and '%s'"
                            % (type(self), type(other)))
        return self.seq == other.seq