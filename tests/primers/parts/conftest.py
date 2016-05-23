import pytest

from primers.parts.models import DNABarcode1, DNABarcode2, \
    IlluminaReadingAdaptor1, IlluminaReadingAdaptor2, \
    IlluminaReadingAdaptor1ForHead, IlluminaReadingAdaptor1ForTail, \
    IlluminaReadingAdaptor2ForHead, IlluminaReadingAdaptor2ForTail



@pytest.fixture()
def dnabarcode1(transactional_db):
    b1 = DNABarcode1.objects.create(
        name='D508',
        _sequence='GTACTGAC'
    )
    # So our objects don't have "special" objects in fields
    b1 = DNABarcode1.objects.get(pk=b1.pk)
    return b1


@pytest.fixture()
def dnabarcode2(transactional_db):
    b2 = DNABarcode2.objects.create(
        name='D710',
        _sequence='TCCGCGAA'
    )
    # So our objects don't have "special" objects in fields
    b2 = DNABarcode2.objects.get(pk=b2.pk)
    return b2


@pytest.fixture()
def dnabarcode1_a(transactional_db):
    b3 = DNABarcode1.objects.create(
        name='D502',
        _sequence='ATAGAGGC'
    )
    # So our objects don't have "special" objects in fields
    b3 = DNABarcode1.objects.get(pk=b3.pk)
    return b3


@pytest.fixture()
def dnabarcode2_a(transactional_db):
    b4 = DNABarcode2.objects.create(
        name='D718',
        _sequence='TGGGAGCC'
    )
    # So our objects don't have "special" objects in fields
    b4 = DNABarcode2.objects.get(pk=b4.pk)
    return b4


@pytest.fixture()
def illuminareadingadaptor1(transactional_db):
    ira1 = IlluminaReadingAdaptor1.objects.create(
        name='Illumina Standard Reading Adaptor1',
        _sequence='ACACTCTTTCCCTACACGACGCTCTTCCGATCT'
    )
    # So our objects don't have "special" objects in fields
    ira1 = IlluminaReadingAdaptor1.objects.get(pk=ira1.pk)
    return ira1


@pytest.fixture()
def illuminareadingadaptor2(transactional_db):
    ira2 = IlluminaReadingAdaptor2.objects.create(
        name='Illumina Standard Reading Adaptor2',
        _sequence='AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC'
    )
    # So our objects don't have "special" objects in fields
    ira2 = IlluminaReadingAdaptor2.objects.get(pk=ira2.pk)
    return ira2


@pytest.fixture()
def illuminareadingadaptor1fortail(illuminareadingadaptor1):
    irac1 = IlluminaReadingAdaptor1ForTail.objects.create(
        ira=illuminareadingadaptor1,
        tail_length=22,
    )
    # So our objects don't have "special" objects in fields
    irac1 = IlluminaReadingAdaptor1ForTail.objects.get(pk=irac1.pk)
    return irac1


@pytest.fixture()
def illuminareadingadaptor1forhead(illuminareadingadaptor1):
    irac1 = IlluminaReadingAdaptor1ForHead.objects.create(
        ira=illuminareadingadaptor1,
        head_length=29,
    )
    # So our objects don't have "special" objects in fields
    irac1 = IlluminaReadingAdaptor1Cuts.objects.get(pk=irac1.pk)
    return irac1


@pytest.fixture()
def illuminareadingadaptor2fortail(illuminareadingadaptor2):
    irac2 = IlluminaReadingAdaptor2ForTail.objects.create(
        ira=illuminareadingadaptor2,
        tail_length=22,
    )
    # So our objects don't have "special" objects in fields
    irac2 = IlluminaReadingAdaptor2ForTail.objects.get(pk=irac2.pk)
    return irac2


@pytest.fixture()
def illuminareadingadaptor2forhead(illuminareadingadaptor2):
    irac2 = IlluminaReadingAdaptor2ForHead.objects.create(
        ira=illuminareadingadaptor2,
        head_length=30,
    )
    # So our objects don't have "special" objects in fields
    irac2 = IlluminaReadingAdaptor2Cuts.objects.get(pk=irac2.pk)
    return irac2

