import pytest
from pywikipathways.download_pathway_archive import *

def test_successful_download():
    filename = download_pathway_archive(date='current', organism='Mus musculus', format='gpml')
    assert filename == 'wikipathways-20240910-gpml-Mus_musculus.zip'

    filename = download_pathway_archive(date='current', organism='Mus musculus', format='gmt')
    assert filename == 'wikipathways-20240910-gmt-Mus_musculus.gmt'

    filename = download_pathway_archive(date='current', organism='Mus musculus', format='svg')
    assert filename == 'wikipathways-20240910-svg-Mus_musculus.zip'
    
