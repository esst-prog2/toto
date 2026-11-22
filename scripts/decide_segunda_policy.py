"""Phase 6 source-bound decisions and provisional accounting, no match export.

No network, original mutation, standardized CSV, application integration or
training. The additional Deportivo hold is a proposal awaiting user review.
"""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import date
from pathlib import Path

from scripts import verify_segunda_review as review

ROOT, PRIVATE, base = review.ROOT, review.PRIVATE, review.base
BASELINE = 'phase6_protected_before.json'
POLICY = 'phase6_decision_policy.json'
ASSESSMENT = 'phase6_policy_assessment.json'
APPROVAL = 'USER_APPROVED_PHASE6'
PROPOSED = 'PROPOSED_CONSERVATIVE_HOLD_PENDING_USER_REVIEW'
HASHES = {
    2014:'939f23a767e78e96dc62d640a8834967ff28b974e8e73c9766a51c2b95222faa',
    2018:'5d28c6719b973971f88103f033fa9d10bdc7a7904f30c84fa34d1ed7e299cd14',
    2019:'4f8f228e2df9b1e7e4c2bb8dbf2834523ef933ac535ab75782b35352c2d3b8fd',
    2024:'0d55243481eabe5e836d86c979fbd600033e10a07946cc9bce224ce13bd183d4'}
SUPPLEMENTS = (
    (745,'2025-05-31','Málaga CF','Burgos CF','2-2'),
    (747,'2025-06-01','SD Huesca','CD Eldense','3-2'),
    (748,'2025-06-01','UD Almería','CD Tenerife','2-0'),
    (749,'2025-06-01','FC Cartagena','CD Mirandés','1-3'),
    (750,'2025-06-01','Deportivo La Coruña','Elche CF','0-4'),
    (751,'2025-06-01','Real Oviedo','Cádiz CF','2-1'),
    (752,'2025-06-01','Levante UD','SD Eibar','1-0'),
    (753,'2025-06-01','Racing Santander','Granada CF','2-1'),
    (754,'2025-06-01','Córdoba CF','Albacete','1-1'))
AWARD_LINES = (376,401,419,430,453,469,483,501,518,536,554,573,591,608,626,641,660,676,695,711,733)
SPECIALS = (
    (2014,82,'2014-09-21','CA Osasuna','RCD Mallorca','6-4','RETAIN_UNUSUAL_SCORE'),
    (2014,291,'2014-12-20','CD Numancia','CD Lugo','6-6','RETAIN_UNUSUAL_SCORE'),
    (2019,346,'2020-06-10','Rayo Vallecano','Albacete','1-0','COMPLETED_INTERRUPTED_MATCH'),
    (2019,722,'2020-08-07','Deportivo La Coruña','CF Fuenlabrada','2-1','CONDITIONAL_HOLD_OUT'))


def day(value):
    if not isinstance(value,str) or date.fromisoformat(value).isoformat()!=value:
        raise ValueError('Canonical ISO calendar day required')
    return date.fromisoformat(value)


def score(value):
    if not isinstance(value,str): raise ValueError('Complete full-time score required')
    parts=value.split('-')
    if len(parts)!=2 or any(not x.isascii() or not x.isdecimal() for x in parts):
        raise ValueError('Complete nonnegative numeric score required')
    return tuple(int(x) for x in parts)


# Frozen Phase 5 claim/document digests; no documentary text or datasets embedded.
CLAIM_HASHES = {(2014, 82): '02778bb77bd38bf88710161507322be80f1faacdf82138d50d715e209bd67f15',
 (2014, 291): 'b98eefbb73f79f6de8d46565f6c26c6f86e6f0fc1aabf106e5d95ca0fdb151d5',
 (2018, 376): '1f775408266c59c4aac8a6ffcc7e1efe1e65e9228c5fbdb68dc312ca022ab652',
 (2018, 401): '693eff91ede691cbc28b541d385d85f6fd92a705d57287db2708a8dd74754d58',
 (2018, 419): 'd6e303ee547145eba3d45d54b65952318d440e6af2eff308e9d76b9bd2a46802',
 (2018, 430): '5df62dc1556ebdd133fc8d5ddf491545530beac38bee5b3cce5e183eda359ba6',
 (2018, 453): '91604942c424c09732f2b54c80f5a6eeee451931147bd0e2a7d56e7c2fcc30bd',
 (2018, 469): '72dfb31e423f969d34278ea7491131ca955c6d0a07b36226fc6030771b968417',
 (2018, 483): '1ec160b1b010229629ed615648bcaa5d40101b0a0eee9dcc2d83353fe1a1fae5',
 (2018, 501): '8fc99c1df4c26f3e234c92eb076fe373247a4f13c260917cd1586fdcba911095',
 (2018, 518): '0993219091d2197d3896ba413d5df3cabc6d0405163bc0a59a64c512708aa08b',
 (2018, 536): '8ee30dbd6f04902056a824834c965f050d82b88b7eab4e637049f345462dc6e6',
 (2018, 554): '31bb056503ec81d405c40b08a0cc3d717912bac875d360e5a283fd753d8171b6',
 (2018, 573): '927081b35db7a68ba794249590c3406025c5ff5ce2b5a0878fa91d7f38e4e5ae',
 (2018, 591): '89746b91412847f6aca947d997d654d6b3d5717ac6c4382fa283246c32859211',
 (2018, 608): '0b4c5677f4902b0887d5cdedaaac0843bdc90fae0da35644f04ee4b7a5a82bc1',
 (2018, 626): '07bc8713d9ae8ae338c9c718e0bda9e301771e5eceb9d4c3647c12d9e17fe3e1',
 (2018, 641): 'f45548de09b4f40d901d3f4fe8582807ae64cb31671299d480b733d583d7223a',
 (2018, 660): '071f62bbd76416233e1bfffa474dc7f27eac9bd890c2a3259a3b73db1ad41a3a',
 (2018, 676): 'e01af45589759d1534c90878f548a12f425e173dc42c2ec5e542f24588df2907',
 (2018, 695): '55f2c57e67dfe57bfc32d080025374164439486bf9b9d080400aa71b476192e1',
 (2018, 711): '4da069baeff9123902ce2437e7248ec490835dbebcb4beeabf81f2cc8b85ad72',
 (2018, 733): '1244f02f13722d63f5fe088d6d68435fbd03a6f0562c7d2ec35b23bb0d2b57a3',
 (2019, 346): '87a1e0b465764382317a2eaa9308f809288436d3601d7749d11b295b1adad00b',
 (2019, 722): '0179e47730d7bc38a76fa51d7f6f711481bca21b3a8d513fc32ed882ad847f9d',
 (2024, 745): 'db0463bbf0987c5eab9cbfb0434af6bb8e1dc058be75d728af500953a254800a',
 (2024, 747): '4bead2d6d624fe892de5498cfe6cbf08169c85a39954a9f282923419d5e175e2',
 (2024, 748): '32b3d3fc8147d491afb35b59efc78661d5168f87b83ec8a8dc92e53f0e5a7ab0',
 (2024, 749): 'be75cc3da97d0ad58cef53bfa028756750e1ba86f743ebdfc933e6600810307e',
 (2024, 750): '8a64a119039030f6bfba063fb7a5ba14f4ba614f5fbe6ff60f52e51a7eb7f4f2',
 (2024, 751): 'f10925baa7a4a49ea8e60e1059c1d183b99095163d0e1c8e3c77c1a9eab3e2b8',
 (2024, 752): '9cd1dd66c74ef08935085aff062b60cffd2950ff0920ccedcd1c2287e7b1ef27',
 (2024, 753): '3663f8c551b2539c3ad32c8b0c6db78bab61a7802137a11d13a8903ca78febd7',
 (2024, 754): 'f9861a3ba7f6a5ef9eedd65f593fa590066b4bcae8ba6c635793cf0ac591688c'}
EVIDENCE_BINDINGS = {'cordoba': ('https://cordopolis.eldiario.es/deportes/ccf/noche-aplausos-poste-empate-cerrar-telon-arcangel_129_12347871.html',
             'dc69ccad25f38bbca27dc562b4911bc1ccd26df83d07374e32356881bee428a2',
             'DOCUMENT_OPENED'),
 'dep_archive': ('https://iusport.com/archive/111994/competicion-acata-la-resolucion-del-tad-y-archiva-el-expediente-al-fuenlabrada',
                 '632ce71f1fd152568a1fb95d2d635c20d9ea5c21646c5dc1fc26596c537dfd4a',
                 'DOCUMENT_OPENED'),
 'dep_result': ('https://www.rtve.es/deportes/20200807/deportivo-fuenlabrada-penalti-ultimo-minuto-cronica-segunda/2038303.shtml',
                'dac4429f226aec8275dfd9de9dddad34cf39d8feb3eb4e95dc5eeeec50fd53b3',
                'DOCUMENT_OPENED'),
 'dep_schedule': ('https://rfef.es/sites/default/files/sanciones/resolucion_comite_de_competicion_-_fecha_rc_deportivo-cf_fuenlabrada.pdf',
                  'c389af0877b4f499923f5d69c3ef42ca832df28c9706baf08cf8def8b4d7079c',
                  'DOCUMENT_OPENED'),
 'dep_tad': ('https://iusport.com/archive/115846/el-tad-confirma-el-fallo-del-juez-de-laliga-y-pone-punto-y-final-al-caso-depor-fuenlabrada',
             '05b276e302478752f75d0a0690ff163458ffe01437bac7fe68f84f5f8795f358',
             'DOCUMENT_OPENED'),
 'high64': ('https://www.laliga.com/noticias/empacho-de-goles-y-remontada-en-el-sadar',
            '318d6dd2064963f911994a2d6ed1da5748148f64d5c630ed32fb5299a642dc0b',
            'DOCUMENT_OPENED'),
 'high66': ('https://www.laliga.com/noticias/numancia-y-lugo-empatan-en-un-partido-historico',
            '79ee4f33591f6eb360b7b94c9d574dd5edb188cadee781a7e48f292c45458967',
            'DOCUMENT_OPENED'),
 'missing42': ('https://www.laliga.com/en-BR/laliga-hypermotion/results/2024-25/gameweek-42',
               '1350501db9ff477aff08a64806f765c620896cc5d91aec1a2f99358403f30079',
               'DOCUMENT_OPENED'),
 'rayo_appeal': ('https://rfef.es/sites/default/files/pdf/resolucion_apelacion_rayo-albacete.pdf',
                 'a7dfdf256caa443ad746f85d9962ea93cc3743770f52c3c5fc4be81a373b5ddb',
                 'DOCUMENT_OPENED'),
 'rayo_result': ('https://www.rayovallecano.es/noticias/rayo-1-albacete-balompie-0-video-resumen',
                 'e96c6bb957fbc69d276e93d54dac93b97766039df9e45260394a19c23fc8a9fc',
                 'DOCUMENT_OPENED'),
 'rayo_schedule': ('https://rfef.es/es/noticias/comite-competicion-fija-rayo-albacete-jornada-20-dia-10-junio',
                   'c2b454c0326ef39ebfd9d07b8abbc4692728e86dad19869952c4ec4e2c8e283e',
                   'DOCUMENT_OPENED'),
 'reus_awards': ('https://as.com/futbol/2019/02/07/segunda/1549543584_310755.html',
                 'e56141ab06e7545768c69dc09ec7dd2f78d166d2240ca8b7ebc5dc6f500e7ec7',
                 'DOCUMENT_OPENED'),
 'reus_court': ('https://iusport.com/archive/116565/la-justicia-da-la-razon-al-tad-y-a-laliga-y-ratifica-la-expulsion-del-reus',
                '5724668d733a518d836b518ce3294aac2c3b256fb56a9516719982e9e38df9c8',
                'DOCUMENT_OPENED'),
 'reus_expulsion': ('https://www.laliga.com/noticias/nota-informativa-164',
                    '92027ac64fb3494b25cfb1178448458478867a47b6b756fcb59511e351682709',
                    'DOCUMENT_OPENED'),
 'reus_suspend': ('https://www.laliga.com/noticias/nota-informativa-cf-reus-deportiu',
                  '01649967e6802c1727082b40ad6e3c6307e1f99dcb48d04621eb8eeb2bf97826',
                  'DOCUMENT_OPENED'),
 'reus_tad': ('https://iusport.com/archive/85744/el-tad-rechaza-definitivamente-el-recurso-del-reus-sobre-su-exclusion',
              '830fdefefae60838f92c9dd0aaac4703fe113ca003e69e4b4f8f34d6d0137fd3',
              'INDEX_ONLY')}
AWARDS = {(2018, 376): ('2019-01-19', 'CF Reus Deportiu', 'UD Las Palmas', '0-1'),
 (2018, 401): ('2019-01-27', 'Albacete', 'CF Reus Deportiu', '1-0'),
 (2018, 419): ('2019-02-03', 'CF Reus Deportiu', 'Elche CF', '0-1'),
 (2018, 430): ('2019-02-09', 'Gimnàstic de Tarragona', 'CF Reus Deportiu', '1-0'),
 (2018, 453): ('2019-02-17', 'CF Reus Deportiu', 'UD Almería', '0-1'),
 (2018, 469): ('2019-02-24', 'Granada CF', 'CF Reus Deportiu', '1-0'),
 (2018, 483): ('2019-03-03', 'CF Reus Deportiu', 'CD Tenerife', '0-1'),
 (2018, 501): ('2019-03-10', 'CD Lugo', 'CF Reus Deportiu', '1-0'),
 (2018, 518): ('2019-03-17', 'CF Reus Deportiu', 'Deportivo La Coruña', '0-1'),
 (2018, 536): ('2019-03-24', 'Extremadura UD', 'CF Reus Deportiu', '1-0'),
 (2018, 554): ('2019-03-31', 'CF Reus Deportiu', 'Cádiz CF', '0-1'),
 (2018, 573): ('2019-04-07', 'RCD Mallorca', 'CF Reus Deportiu', '1-0'),
 (2018, 591): ('2019-04-14', 'CF Reus Deportiu', 'Real Oviedo', '0-1'),
 (2018, 608): ('2019-04-21', 'Real Zaragoza', 'CF Reus Deportiu', '1-0'),
 (2018, 626): ('2019-04-28', 'CF Reus Deportiu', 'AD Alcorcón', '0-1'),
 (2018, 641): ('2019-05-05', 'Córdoba CF', 'CF Reus Deportiu', '1-0'),
 (2018, 660): ('2019-05-12', 'CA Osasuna', 'CF Reus Deportiu', '1-0'),
 (2018, 676): ('2019-05-19', 'CF Reus Deportiu', 'Málaga CF', '0-1'),
 (2018, 695): ('2019-05-26', 'CD Numancia', 'CF Reus Deportiu', '1-0'),
 (2018, 711): ('2019-06-02', 'CF Reus Deportiu', 'Sporting Gijón', '0-1'),
 (2018, 733): ('2019-06-09', 'Rayo Majadahonda', 'CF Reus Deportiu', '1-0')}


def expected_specs():
    specs={(2024,n):dict(action='SUPPLEMENT_MISSING_SCORE',date=d,home=h,away=a,FT=None,result=s)
           for n,d,h,a,s in SUPPLEMENTS}
    specs.update({(y,n):dict(action=act,date=d,home=h,away=a,FT=s,result=s)
                  for y,n,d,h,a,s,act in SPECIALS})
    specs.update({key:dict(action='UNRESOLVED_HOLD_OUT',date=d,home=h,away=a,FT=s) for key,(d,h,a,s) in AWARDS.items()})
    return specs


def source_key(record):
    return int(record['season'][:4]),record['source_line']


def protected(directory=PRIVATE, root=ROOT):
    previous=review.protect(directory,root)
    frozen=review.read(directory/BASELINE)
    if len(frozen['files'])!=68:raise ValueError('Phase 6 baseline scope changed')
    for name,digest in frozen['files'].items():
        path=root/name
        if not path.resolve().is_relative_to(root.resolve()) or base.sha(path.read_bytes())!=digest:
            raise ValueError('Protected Phase 2–5 artifact changed: '+name)
    prefix=frozen['planning_log'];raw=(root/'PLANNING_LOG.md').read_bytes()
    if len(raw)<prefix['bytes'] or base.sha(raw[:prefix['bytes']])!=prefix['sha256']:
        raise ValueError('Planning history changed')
    return dict(previous=previous,phase2_5_files=len(frozen['files']))


def validate_case(case):
    r=case['original'];key=source_key(r);spec=expected_specs().get(key)
    if spec is None or case['action']!=spec['action']:raise ValueError('Unapproved exceptional action/source location')
    year,line=key;file=f'openfootball/espana/{year}-{(year+1)%100:02}/2-liga2.txt'
    expected_id=review.structural.source_id(file,HASHES[year],line)
    if (r['source_file']!=file or r['source_sha256']!=HASHES[year] or
            r['source_fixture_id']!=expected_id or case['fixture_id']!=expected_id or
            r['source_commit']!=review.structural.base.PIN or r['season']!=f'{year}/{year+1}'):
        raise ValueError('Decision provenance/source identity mismatch')
    day(r['date'])
    if case['approval']!=(PROPOSED if case['action']=='CONDITIONAL_HOLD_OUT' else APPROVAL):
        raise ValueError('Decision approval strength changed')
    if (not case['evidence'] or case['phase5_status'] not in review.STATUSES or
            case['phase5_claim_sha256']!=CLAIM_HASHES[key]):
        raise ValueError('Missing bound historical evidence')
    for e in case['evidence']:
        if EVIDENCE_BINDINGS.get(e['id'])!=(e['url'],e['source_entry_sha256'],e['access']):
            raise ValueError('Independent evidence identity/hash changed')
    expected_evidence = ({'missing42'} if line!=754 else {'cordoba'}) if spec['action']=='SUPPLEMENT_MISSING_SCORE' else (
        {'reus_expulsion','reus_awards','reus_court','reus_tad'}|({'reus_suspend'} if line==376 else set())) if spec['action']=='UNRESOLVED_HOLD_OUT' else (
        {'high64'} if key==(2014,82) else {'high66'} if key==(2014,291) else
        {'rayo_result','rayo_schedule','rayo_appeal'} if key==(2019,346) else
        {'dep_result','dep_schedule','dep_archive','dep_tad'})
    if len(case['evidence'])!=len(expected_evidence) or {e['id'] for e in case['evidence']}!=expected_evidence:
        raise ValueError('Required corroboration omitted or duplicated')
    if any(r[k]!=spec[k] for k in ('date','home','away','FT')):
        raise ValueError('Approved fixture facts changed')
    event=case['event_dates']
    for value in event.values():
        if value is not None:day(value)
    action=case['action']
    expected_event=dict(source=r['date'],scheduled=None,kickoff=None,completion=None,
                        individual_administrative_decision=None,expulsion_decision=None,intermediate_schedule=None)
    if action=='UNRESOLVED_HOLD_OUT':expected_event['expulsion_decision']='2019-01-28'
    else:expected_event.update(kickoff=r['date'],completion=r['date'])
    if action=='COMPLETED_INTERRUPTED_MATCH':expected_event['kickoff']='2019-12-15'
    if action=='CONDITIONAL_HOLD_OUT':expected_event.update(scheduled='2020-07-20',intermediate_schedule='2020-08-05')
    if event!=expected_event:raise ValueError('Approved event-date semantics changed')
    action=case['action'];effective=case['effective_result_date']
    if action=='UNRESOLVED_HOLD_OUT':
        if (not r['source_marked_awarded'] or 'CF Reus Deportiu' not in (r['home'],r['away']) or
                r['annotation']!='[awarded]' or case['phase5_status']!='UNRESOLVED' or
                case['result'] is not None or effective is not None or case['finality']!='UNRESOLVED'):
            raise ValueError('Unresolved award cannot acquire a played result/availability')
        if score(r['FT']) not in {(0,1),(1,0)}:raise ValueError('Original Reus award changed')
        if any(case['event_dates'][k] is not None for k in ('kickoff','completion','individual_administrative_decision')):
            raise ValueError('Unknown individual award dates inferred')
    else:
        if any(r[k]!=spec[k] for k in ('date','home','away','FT')):
            raise ValueError('Approved fixture facts changed')
        if r['source_marked_awarded']:raise ValueError('Played decision bound to award')
        if case['result']!=spec['result']:raise ValueError('Approved result changed')
        score(case['result'])
        if case['phase5_status']!='VERIFIED':raise ValueError('Played exception/supplement lacks verified evidence')
        if case['event_dates']['completion']!=spec['date']:
            raise ValueError('Verified playing/completion day changed')
        if action=='CONDITIONAL_HOLD_OUT':
            if effective is not None or case['finality']!='PARTIAL_SECONDARY_CLOSURE_EVIDENCE':
                raise ValueError('Conditional hold cannot silently become accepted')
        elif effective!=spec['date'] or case['finality']!='NO_FINAL_OUTCOME_CONFLICT_IDENTIFIED_NOT_EXHAUSTIVELY_CERTIFIED':
            raise ValueError('Approved effective day/finality changed')
        if action=='COMPLETED_INTERRUPTED_MATCH':
            if case['event_dates']['kickoff']!='2019-12-15':raise ValueError('Original interrupted kickoff lost')
        elif action=='CONDITIONAL_HOLD_OUT':
            if case['event_dates']['scheduled']!='2020-07-20' or case['event_dates']['intermediate_schedule']!='2020-08-05':
                raise ValueError('Postponement history lost')
        elif case['event_dates']['kickoff']!=spec['date']:
            raise ValueError('Verified playing day lost')


def validate_registry(policy):
    if policy['approval']!=APPROVAL or policy['phase']!=6 or policy['standardized_output_generated'] is not False:
        raise ValueError('Wrong phase/approval or match-export state')
    keys=[];ids=[]
    for c in policy['cases']:
        validate_case(c);keys.append(source_key(c['original']));ids.append(c['fixture_id'])
    if len(set(keys))!=len(keys) or len(set(ids))!=len(ids) or set(keys)!=set(expected_specs()):
        raise ValueError('Missing, extra or duplicate exceptional decision')
    expected_decisions={key:f'SD6-{i:02}' for i,key in enumerate(sorted(expected_specs()),1)}
    if any(c['decision_id']!=expected_decisions[source_key(c['original'])] for c in policy['cases']):
        raise ValueError('Decision identifier missing or rebound')
    holds=sorted(c['fixture_id'] for c in policy['cases'] if c['action']=='UNRESOLVED_HOLD_OUT')
    conditional=sorted(c['fixture_id'] for c in policy['cases'] if c['action']=='CONDITIONAL_HOLD_OUT')
    if policy['unresolved_hold_ids']!=holds or policy['conditional_hold_ids']!=conditional:
        raise ValueError('Hold registry incomplete or conflicting')
    if policy['global_team_mappings']!={}:raise ValueError('Unapproved team identity mapping')
    groups=policy['uncertainty']['identity_groups']
    if (len(groups)!=6 or {g['source_label'] for g in groups}!=review.structural.RESERVES or
            any(g['apply_mapping'] or not g['keep_separate_from_parent'] or g['parent']==g['source_label'] for g in groups)):
        raise ValueError('Reserve identity policy lost or merged')
    return {c['fixture_id']:c for c in policy['cases']}


def assess_record(record, cases, *, identified_final_outcome='NO_CONFLICT_IDENTIFIED',
                  technical_status='STRUCTURAL_PASS', historical_status='UNVERIFIED'):
    """Internal batch primitive; public consumers must use assess with full policy."""
    if identified_final_outcome not in {'NO_CONFLICT_IDENTIFIED','UNRESOLVED'}:
        raise ValueError('Explicit final-outcome conflict state required')
    stored_state=record.get('identified_final_outcome_status','NO_CONFLICT_IDENTIFIED')
    if stored_state not in {'NO_CONFLICT_IDENTIFIED','UNRESOLVED'}:
        raise ValueError('Unknown stored final-outcome conflict state')
    if stored_state=='UNRESOLVED':identified_final_outcome='UNRESOLVED'
    if technical_status not in {'STRUCTURAL_PASS','STRUCTURAL_FAIL'} or historical_status not in {'VERIFIED','PARTIAL','UNVERIFIED','UNRESOLVED'}:
        raise ValueError('Unknown technical/historical classification')
    identity_labels(record['home'],record['away'])
    day(record['date'])
    case=cases.get(record['source_fixture_id'])
    if case is not None and case['original']!=record:raise ValueError('Decision attached to different raw observation')
    if source_key(record) in expected_specs() and case is None:raise ValueError('Required exceptional decision absent')
    if case is not None:validate_case(case)
    source_result=record['FT'];result=source_result;effective=record['date'];basis='SOURCE_PLAYING_DATE_PROXY_NOT_CERTIFIED'
    status='CANDIDATE_NOT_STANDARDIZED';action=case['action'] if case else None
    if source_result is not None:
        h,a=score(source_result)
        if record['hg']!=str(h) or record['ag']!=str(a):raise ValueError('Full-time/numeric score conflict')
    elif record['hg'] is not None or record['ag'] is not None:raise ValueError('Partial goals despite missing FT')
    if action is not None:
        result=case['result'];effective=case['effective_result_date'];basis='APPROVED_VERIFIED_PLAYING_COMPLETION_DAY'
        if action=='UNRESOLVED_HOLD_OUT':status='UNRESOLVED_HOLD_OUT'
        if action=='CONDITIONAL_HOLD_OUT':status='CONDITIONAL_HOLD_OUT_PENDING_REVIEW'
    elif source_result is None:
        status='MISSING_RESULT_HOLD_OUT';effective=None
    if record['source_marked_awarded'] and action!='UNRESOLVED_HOLD_OUT':
        status='UNRESOLVED_ADMINISTRATIVE_HOLD_OUT';effective=None
    if identified_final_outcome=='UNRESOLVED':status='UNRESOLVED_FINAL_OUTCOME_HOLD_OUT';effective=None
    if technical_status=='STRUCTURAL_FAIL':status='TECHNICAL_HOLD_OUT';effective=None
    if status!='CANDIDATE_NOT_STANDARDIZED':effective=None;basis='UNRESOLVED_OR_UNAPPROVED_AVAILABILITY'
    if effective is not None:day(effective)
    return dict(fixture_id=record['source_fixture_id'],screening_status=status,
                exception_policy_screenable=status=='CANDIDATE_NOT_STANDARDIZED',
                effective_result_date=effective,availability_basis=basis,
                source_result=source_result,policy_result=result,score_supplement=action=='SUPPLEMENT_MISSING_SCORE',
                technical_acceptance=technical_status,historical_verification=historical_status,
                final_outcome_status=identified_final_outcome if status=='CANDIDATE_NOT_STANDARDIZED' else 'UNRESOLVED_OR_PENDING_DECISION',
                model_training_suitability='NOT_CLEARED',licensing_clearance='UNRESOLVED')


def assess(record, policy, **classifications):
    return assess_record(record,validate_registry(policy),**classifications)


def identity_labels(home, away, mappings=None):
    if mappings not in (None,{}):raise ValueError('Unapproved or ambiguous identity mapping')
    if not isinstance(home,str) or not isinstance(away,str) or not home.strip() or not away.strip() or home==away:
        raise ValueError('Missing or colliding participant identities')
    return home,away


def known_strictly_before(availability_date, prediction_date):
    prediction=day(prediction_date)
    return availability_date is not None and day(availability_date)<prediction


def training_allowed(assessment, prediction_date):
    return (known_strictly_before(assessment['effective_result_date'],prediction_date)
            and assessment['exception_policy_screenable'] is True
            and assessment['screening_status']=='CANDIDATE_NOT_STANDARDIZED'
            and assessment['final_outcome_status']=='NO_CONFLICT_IDENTIFIED'
            and assessment['availability_basis']=='APPROVED_VERIFIED_PLAYING_COMPLETION_DAY'
            and assessment['model_training_suitability']=='CLEARED' and assessment['licensing_clearance']=='CLEARED')


def make_policy(report, queue, ledger):
    rows={source_key(r):r for r in report['records']}
    if len(rows)!=len(report['records']):raise ValueError('Duplicate physical source binding')
    evidence=review.sources(ledger['sources']);claims={c['source_fixture_id']:c for c in ledger['fixtures']}
    if len(claims)!=len(ledger['fixtures']):raise ValueError('Duplicate historical claim')
    cases=[]
    for key,spec in sorted(expected_specs().items()):
        r=rows[key];c=claims[r['source_fixture_id']]
        review.check_claim(c,r,evidence)
        action=spec['action'];held=action in {'UNRESOLVED_HOLD_OUT','CONDITIONAL_HOLD_OUT'}
        event=dict(source=r['date'],scheduled=None,kickoff=None,completion=None,
                   individual_administrative_decision=None,expulsion_decision=None,intermediate_schedule=None)
        if not r['source_marked_awarded']:event.update(kickoff=r['date'],completion=r['date'])
        if action=='UNRESOLVED_HOLD_OUT':event['expulsion_decision']='2019-01-28'
        if action=='COMPLETED_INTERRUPTED_MATCH':event['kickoff']='2019-12-15'
        if action=='CONDITIONAL_HOLD_OUT':event.update(scheduled='2020-07-20',intermediate_schedule='2020-08-05')
        if action!='UNRESOLVED_HOLD_OUT':
            wanted={k:r[k] for k in ('date','home','away')};wanted['FT']=spec['result']
            if c['independent_facts']!=wanted:raise ValueError('Supplement/exception disagrees with independent facts')
        item=dict(decision_id=f'SD6-{len(cases)+1:02}',fixture_id=r['source_fixture_id'],original=deepcopy(r),
                  action=action,approval=PROPOSED if action=='CONDITIONAL_HOLD_OUT' else APPROVAL,
                  result=spec.get('result'),effective_result_date=None if held else spec['date'],event_dates=event,
                  phase5_status=c['status'],phase5_claim_sha256=base.sha(base.encode(c)),
                  evidence=[dict(id=e,url=evidence[e]['url'],access=evidence[e]['access'],
                                 source_entry_sha256=base.sha(base.encode(evidence[e]))) for e in c['evidence']],
                  finality='UNRESOLVED' if action=='UNRESOLVED_HOLD_OUT' else
                  'PARTIAL_SECONDARY_CLOSURE_EVIDENCE' if action=='CONDITIONAL_HOLD_OUT' else
                  'NO_FINAL_OUTCOME_CONFLICT_IDENTIFIED_NOT_EXHAUSTIVELY_CERTIFIED',
                  source_score_blank_preserved=action=='SUPPLEMENT_MISSING_SCORE')
        validate_case(item);cases.append(item)
    uncertainty=dict(rounds=deepcopy(ledger['rounds']),diagnostic_outlier_ids=sorted(
        x['fixture']['source_fixture_id'] for x in queue['records'] if 'DIAGNOSTIC_DATE_OUTLIER' in x['categories']),
        source_order_reversals=[dict(season=s['season'],**x) for s in report['seasons'] for x in s['validation']['source_order_reversals']],
        partial_fixture_ids=sorted(c['source_fixture_id'] for c in ledger['fixtures'] if c['status']=='PARTIAL'),
        sample_selection_sha256=None,identity_groups=deepcopy(ledger['identities']),gaps=deepcopy(report['gaps']))
    policy=dict(phase=6,approval=APPROVAL,cases=cases,
                unresolved_hold_ids=sorted(c['fixture_id'] for c in cases if c['action']=='UNRESOLVED_HOLD_OUT'),
                conditional_hold_ids=sorted(c['fixture_id'] for c in cases if c['action']=='CONDITIONAL_HOLD_OUT'),
                global_team_mappings={},uncertainty=uncertainty,standardized_output_generated=False,
                ordinary_policy='Unchanged source playing-date proxy; unverified history/round context alone is not exclusion. Not demonstrable availability certification.',
                chronological_rule='Only outcomes known strictly before prediction calendar day; no same-day outcomes, round-order chronology or earlier kickoff leakage.',
                proposed_deportivo_hold='Played 2-1 on August7 verified; operative finality/availability insufficiently established. Conditional hold pending user evidence-based review; not an approved permanent exclusion.',
                model_training_clearance='NOT_CLEARED',licensing_clearance='UNRESOLVED')
    validate_registry(policy)
    return policy


def build(directory=PRIVATE, root=ROOT):
    protection=protected(directory,root)
    for name,raw in review.build(directory,root).items():
        if (directory/name).read_bytes()!=raw:raise ValueError('Frozen Phase 5 assessment no longer reproduces')
    report=review.read(directory/review.structural.REPORT);queue=review.read(directory/review.structural.QUEUE)
    ledger=review.read(directory/review.LEDGER);policy=make_policy(report,queue,ledger)
    policy['uncertainty']['sample_selection_sha256']=base.sha((directory/review.SELECTION).read_bytes())
    cases=validate_registry(policy);history={c['source_fixture_id']:c['status'] for c in ledger['fixtures']}
    counts=Counter();seasons={};supplements=0
    for r in report['records']:
        result=assess_record(r,cases,historical_status=history.get(r['source_fixture_id'],'UNVERIFIED'))
        status=result['screening_status'];counts[status]+=1
        seasons.setdefault(r['season'],Counter())[status]+=1
        supplements+=result['score_supplement']
    if sum(counts.values())!=len(report['records']):raise ValueError('Observation reconciliation failed')
    assessment=dict(phase=6,source_observations=len(report['records']),source_score_bearing=sum(r['FT'] is not None for r in report['records']),
                    source_blank_scores=sum(r['FT'] is None for r in report['records']),explicit_decisions=len(cases),
                    action_counts=dict(Counter(c['action'] for c in cases.values())),provisional_counts=dict(counts),
                    season_counts={s:dict(c) for s,c in seasons.items()},evidence_backed_supplements=supplements,
                    uncertainty_counts=dict(rounds=len(policy['uncertainty']['rounds']),round_classifications=dict(Counter(c['status'] for c in ledger['rounds'])),
                                            affected_round_observations=len({i for c in ledger['rounds'] for i in c['fixture_ids']}),
                                            outliers=len(policy['uncertainty']['diagnostic_outlier_ids']),source_order_reversals=len(policy['uncertainty']['source_order_reversals']),
                                            partial_individual_claims=len(policy['uncertainty']['partial_fixture_ids']),reserve_observations=len({i for g in ledger['identities'] for i in g['fixture_ids']})),
                    preservation=protection,standardized_rows_written=0,training_cleared=0,licensing_cleared=0,
                    policy_sha256=base.sha(base.encode(policy)),input_sha256={n:base.sha((directory/n).read_bytes()) for n in
                     [BASELINE,review.LEDGER,review.OUTPUT,review.MATRIX,review.SELECTION,review.structural.REPORT,review.structural.QUEUE]})
    return {POLICY:base.encode(policy),ASSESSMENT:base.encode(assessment)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True);mode.add_argument('--write',action='store_true');mode.add_argument('--check',action='store_true')
    parser.add_argument('--output-directory',type=Path,default=PRIVATE);args=parser.parse_args()
    outputs=build();target=args.output_directory
    for name,raw in outputs.items():
        path=target/name
        if path.exists() and path.read_bytes()!=raw:raise ValueError('Policy output differs; no overwrite: '+name)
        if args.check and not path.exists():raise ValueError('Missing policy output: '+name)
    if args.write:
        for name,raw in outputs.items():
            if not (target/name).exists():base.save(target/name,raw)
    for name,raw in outputs.items():print(name,base.sha(raw))


if __name__=='__main__':main()
