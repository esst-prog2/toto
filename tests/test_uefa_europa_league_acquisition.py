"""Synthetic Phase 1 boundary tests; no private match data or live requests."""
import json
from urllib.request import Request
import pytest
from scripts import acquire_uefa_europa_league as a


@pytest.fixture
def fixture(tmp_path, monkeypatch):
    monkeypatch.setattr(a, 'ROOT', tmp_path)
    base=tmp_path/'data/private/europe/europa_league/phase1';base.mkdir(parents=True)
    raw=b'= UEFA Europa League synthetic\n'
    item=dict(url='https://raw.githubusercontent.com/example/repo/'+'a'*40+'/el.txt',path='originals/el.txt',publisher='synthetic',kind='fixture',max_bytes=1000,encoding='utf-8',contains='Europa',permission_reference='LICENSE',permission_sha256=a.sha(b'CC0'),permission_basis='synthetic permission')
    (base/'LICENSE').write_bytes(b'CC0')
    (base/'LICENSE.provenance.json').write_bytes(a.encode({'sha256':a.sha(b'CC0')}))
    p=base/item['path'];p.parent.mkdir();p.write_bytes(raw)
    receipt=dict(item,sha256=a.sha(raw),bytes=len(raw),status=200,final_url=item['url'],retrieved_at_utc='2026-11-27T12:00:00Z')
    p.with_name(p.name+'.provenance.json').write_bytes(a.encode(receipt))
    return base,item,p


def test_cache_replay_never_opens_network(fixture,monkeypatch):
    base,item,p=fixture
    monkeypatch.setattr(a,'build_opener',lambda *args:pytest.fail('cached replay used network'))
    assert a.acquire(item,base,True)['sha256']==a.sha(p.read_bytes())


@pytest.mark.parametrize('mutation',['bytes','receipt','permission','date','partial'])
def test_tampering_rejected(fixture,mutation):
    base,item,p=fixture;r=p.with_name(p.name+'.provenance.json')
    if mutation=='bytes':p.write_bytes(p.read_bytes()+b'changed')
    elif mutation=='permission':(base/'LICENSE').write_bytes(b'changed')
    elif mutation=='partial':r.unlink()
    else:
        value=json.loads(r.read_bytes())
        if mutation=='date':value.pop('retrieved_at_utc')
        else:value['url']='https://example.org/'
        r.write_bytes(a.encode(value))
    with pytest.raises((ValueError,KeyError)):a.acquire(item,base)


@pytest.mark.parametrize('field,value',[('url','https://www.uefa.com/fixtures'),('url','https://user:pass@api.github.com/x'),('path','../../../../../escape'),('max_bytes',0),('max_bytes',150000001),('permission_basis','')])
def test_invalid_scope_rejected(fixture,field,value):
    base,item,_=fixture;item=dict(item);item[field]=value
    with pytest.raises(ValueError):a.validate(item,base)


def test_html_permission_whitespace_and_tags():
    i=dict(max_bytes=1000,encoding='latin-1',page_copy_grant=True)
    a.check_content(i,b'<p>You are free to <b>copy</b> this\n document in whole or part provided that proper acknowledgement is given.</p>')
    with pytest.raises(ValueError):a.check_content(i,b'publicly readable, no grant')


def test_release_digest_rejected():
    with pytest.raises(ValueError):a.check_content(dict(max_bytes=100,expected_sha256='0'*64),b'wrong zip')


def test_only_official_release_redirect_allowed():
    redirect=a.ReleaseRedirect();req=Request('https://github.com/owner/repo/releases/download/tag/a.zip')
    ok=redirect.redirect_request(req,None,302,'Found',{},'https://release-assets.githubusercontent.com/asset?a=b')
    assert ok.host=='release-assets.githubusercontent.com'
    for target in ('https://example.org/a','http://release-assets.githubusercontent.com/a','https://user:pass@release-assets.githubusercontent.com/a'):
        with pytest.raises(ValueError):redirect.redirect_request(req,None,302,'Found',{},target)


def test_access_stop_does_not_retry(fixture,monkeypatch):
    base,item,p=fixture;p.unlink();p.with_name(p.name+'.provenance.json').unlink()
    stop=base/'access/raw.githubusercontent.com.STOP.json';stop.parent.mkdir();stop.write_text(json.dumps({'error':'HTTP 429'}))
    monkeypatch.setattr(a,'build_opener',lambda *args:pytest.fail('access stop retried'))
    with pytest.raises(RuntimeError):a.acquire(item,base,True)


def test_missing_original_is_offline_by_default(fixture):
    base,item,p=fixture;p.unlink();p.with_name(p.name+'.provenance.json').unlink()
    with pytest.raises(FileNotFoundError):a.acquire(item,base)


@pytest.mark.parametrize('center',[False,True])
def test_mixed_rsssf_container_keeps_only_target_section(center):
    from scripts.assess_uefa_europa_league_phase1 import rsssf_section
    h='<H2><A NAME="uefa">UEFA Cup synthetic</A></H2>'
    if center:h='<center>'+h+'</center>'
    raw=('<h2>Champions League</h2><pre>UNRELATED CL</pre>'+h+'<pre>'+('TARGET EL\n'*20)+'</pre><h2>Super Cup</h2><pre>UNRELATED SC</pre>').encode()
    result=rsssf_section(raw)
    assert 'TARGET EL' in result
    assert 'UNRELATED' not in result
