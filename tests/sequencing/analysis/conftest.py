import pytest
import os
import uuid
from django.conf import settings
import itertools
from Bio import SeqIO

from sequencing.analysis.models import SampleReads, AdamMergedReads, \
    AdamReadsIndex, AdamMarginAssignment, AdamAmpliconReads, \
    AdamMSVariations, AdamHistogram
from sequencing.analysis.models import LEFT, RIGHT
from misc.utils import get_unique_path

from tests.sequencing.runs.conftest import *
from tests.sequencing.analysis.pu_28727_adam_ms_variations import VARS_28727
from tests.lib_prep.workflows.conftest import *
from tests.targeted_enrichment.amplicons.conftest import *
from tests.sequencing.analysis.reads_dict_tools import R1, R2, RM
from tests.flat_dict import FlatDict
from tests.sequencing.analysis.reads_dict import READS_DICT_ADAM, ASSEMBLED, \
    UNASSEMBLED


file_fixtures_path = os.path.join(*(os.path.split(os.path.dirname(os.path.realpath(__file__)))[:-1] + ("ngs_fixtures",)))


@pytest.fixture(scope="session")
def adam_reads_fd():
    return FlatDict(READS_DICT_ADAM, [R1, R2, RM])


@pytest.yield_fixture(scope="session")
def sample_reads_files_d(adam_reads_fd, temp_storage):
    d = {}
    for k, r_d in adam_reads_fd.reads():
        fastq_r1 = get_unique_path("fastq")
        fastq_r2 = get_unique_path("fastq")
        SeqIO.write(r_d[R1], fastq_r1, "fastq")
        SeqIO.write(r_d[R2], fastq_r2, "fastq")
        d[k] = {R1: fastq_r1, R2: fastq_r2}
    yield d
    for f_d in d.itervalues():
        os.unlink(f_d[R1])
        os.unlink(f_d[R2])


@pytest.yield_fixture()
def sample_reads_d(sample_reads_files_d, demultiplexing, magicalpcr1barcodedcontent, magicalpcr1library):
    d = {}
    for k, f_d in sample_reads_files_d.iteritems():
        fastq_r1 = get_unique_path("fastq")
        fastq_r2 = get_unique_path("fastq")
        os.symlink(f_d[R1], fastq_r1)
        os.symlink(f_d[R2], fastq_r2)
        sr = SampleReads.objects.create(
            demux=demultiplexing,
            barcoded_content=magicalpcr1barcodedcontent,
            library=magicalpcr1library,
            fastq1=fastq_r1,
            fastq2=fastq_r2,
        )
        d[k] = sr
    yield d
    for sr in d.itervalues():
        # sr.delete()
        os.unlink(sr.fastq1)
        os.unlink(sr.fastq2)


@pytest.yield_fixture(scope="session")
def adam_merged_reads_files_d(adam_reads_fd, temp_storage):
    d = {}
    for k, s_d in adam_reads_fd.items():
        assembled_fastq = get_unique_path("fastq")
        unassembled_forward_fastq = get_unique_path("fastq")
        unassembled_reverse_fastq = get_unique_path("fastq")
        discarded_fastq = get_unique_path("fastq")
        SeqIO.write(s_d[ASSEMBLED][RM], assembled_fastq, "fastq")
        SeqIO.write(s_d[UNASSEMBLED][R1], unassembled_forward_fastq, "fastq")
        SeqIO.write(s_d[UNASSEMBLED][R2], unassembled_reverse_fastq, "fastq")
        SeqIO.write((), discarded_fastq, "fastq")
        d[k] = {
            ASSEMBLED: assembled_fastq,
            (UNASSEMBLED, R1): unassembled_forward_fastq,
            (UNASSEMBLED, R2): unassembled_reverse_fastq,
            None: discarded_fastq
        }
    yield d
    for f_d in d.itervalues():
        os.unlink(f_d[ASSEMBLED])
        os.unlink(f_d[UNASSEMBLED, R1])
        os.unlink(f_d[UNASSEMBLED, R2])
        os.unlink(f_d[None])


@pytest.yield_fixture()
def adam_merged_reads_d(adam_merged_reads_files_d, sample_reads_d):
    d = {}
    for k, f_d in adam_merged_reads_files_d.iteritems():
        dst_prefix = get_unique_path()
        os.symlink(
            f_d[ASSEMBLED],
            "{}.assembled.fastq".format(dst_prefix)
        )
        os.symlink(
            f_d[None],
            "{}.discarded.fastq".format(dst_prefix)
        )
        os.symlink(
            f_d[UNASSEMBLED, R1],
            "{}.unassembled.forward.fastq".format(dst_prefix)
        )
        os.symlink(
            f_d[UNASSEMBLED, R2],
            "{}.unassembled.reverse.fastq".format(dst_prefix)
        )
        mr = AdamMergedReads.objects.create(
            sample_reads=sample_reads_d[k],
            assembled_fastq="{}.assembled.fastq".format(dst_prefix),
            discarded_fastq="{}.discarded.fastq".format(dst_prefix),
            unassembled_forward_fastq="{}.unassembled.forward.fastq".format(dst_prefix),
            unassembled_reverse_fastq="{}.unassembled.reverse.fastq".format(dst_prefix),
        )
        d[k] = mr
    yield d
    for mr in d.itervalues():
        # mr.delete()
        os.unlink(mr.assembled_fastq)
        os.unlink(mr.discarded_fastq)
        os.unlink(mr.unassembled_forward_fastq)
        os.unlink(mr.unassembled_reverse_fastq)


@pytest.yield_fixture()
def adam_amplicon_reads_files_d(adam_reads_fd, temp_storage):
    d = {}
    for bc, s_d in adam_reads_fd.items():
        # M
        d[bc, "M"] = {}
        for amp, r_d in s_d.sub(ASSEMBLED).reads():
            f_d = {
                RM: get_unique_path("fastq"),
                R1: get_unique_path("fastq"),
                R2: get_unique_path("fastq"),
            }
            for r in [R1, R2, RM]:
                SeqIO.write(r_d[r], f_d[r], "fastq")
            d[bc, "M"][amp] = f_d
        # F
        d[bc, "F"] = {}
        all_amps = set(s_d.sub(ASSEMBLED).keys()) | set(s_d.sub(UNASSEMBLED).keys())
        for amp in all_amps:
            # Assuming there are no amplicons only present in UNASSEMBLED
            f_d = {
                RM: get_unique_path("fastq"),
                R1: get_unique_path("fastq"),
                R2: get_unique_path("fastq"),
            }
            for r in [R1, R2]:
                SeqIO.write(itertools.chain(
                    s_d[ASSEMBLED, amp][r],
                    s_d[UNASSEMBLED, amp][r],
                    ), f_d[r], "fastq")
            SeqIO.write(itertools.chain(
                s_d[ASSEMBLED, amp][RM],
                s_d[UNASSEMBLED, amp][R1],
                ), f_d[RM], "fastq")
            d[bc, "F"][amp] = f_d
    yield d
    for f_d_d in d.itervalues():
        for f_d in f_d_d.itervalues():
            os.unlink(f_d[RM])
            os.unlink(f_d[R1])
            os.unlink(f_d[R2])


@pytest.yield_fixture()
def _chain(adam_amplicon_reads_files_d, adam_merged_reads_d):
    d = {}
    for (bc, inc), f_d_d in adam_amplicon_reads_files_d.iteritems():
        dst_dir = get_unique_path()
        os.mkdir(dst_dir)
        ari = AdamReadsIndex.objects.create(
            merged_reads=adam_merged_reads_d[bc],
            included_reads=inc,  # Merged and unassembled_forward
            index_dump_dir=dst_dir,
            padding=5,
        )
        fake_sam = get_unique_path("sam")
        with open(fake_sam, "wb") as f:
            pass
        ama = AdamMarginAssignment.objects.create(
            reads_index=ari,
            assignment_sam=fake_sam,
        )
        d[bc, inc] = ari, ama
    yield d
    for ari, ama in d.itervalues():
        os.rmdir(ari.index_dump_dir)
        os.unlink(ama.assignment_sam)


@pytest.yield_fixture()
def adam_amplicon_reads_d(adam_amplicon_reads_files_d, _chain, amplicon_d):
    d = {}
    extra_dirs = []
    extra_files = []
    for (bc, inc), f_d_d in adam_amplicon_reads_files_d.iteritems():
        ari, ama = _chain[bc, inc]
        for amp, f_d in f_d_d.iteritems():
            f_d2 = {}
            for r in [R1, R2, RM]:
                f_d2[r] = get_unique_path("fastq")
                os.symlink(f_d[r], f_d2[r])
            aar = AdamAmpliconReads.objects.create(
                margin_assignment=ama,
                amplicon=amplicon_d[amp],  # FIXME
                fastqm=f_d2[RM],
                fastq1=f_d2[R1],
                fastq2=f_d2[R2],
            )
            d[bc, inc, amp] = aar
    yield d
    for aar in d.itervalues():
        # aar.margin_assignment.reads_index.delete()
        # aar.margin_assignment.delete()
        # aar.delete()
        os.unlink(aar.fastqm)
        os.unlink(aar.fastq1)
        os.unlink(aar.fastq2)
