from answer_checker import check_answer
from curriculum import TOPICS,DIFFICULTIES
from question_engine import build_adventure
from scoring import record,summary
from certificate import create_certificate
import leaderboard

def test_equivalent_answers():
    for x in ['1/2','2/4','0.5','50%']:
        assert check_answer(x,'1/2')
    assert check_answer('1 1/2','1.5')
    assert check_answer('1,234','1234')
    for x in ['NaN','inf','1/0','1,2','__import__("os")','0.333']:
        assert not check_answer(x,'1/3')

def test_all_adventures_and_marking():
    for year in [4,5,6]:
        for topic in TOPICS:
            qs=build_adventure(year,'Mixed Cambridge + Malaysian',topic,'All three levels',seed=123)
            assert len(qs)==30
            assert len({q['id'] for q in qs})==30
            results=[]
            for q in qs:
                answer=[p['answer'] for p in q['pairs']] if q['question_type']=='matching' else q['answer']
                assert record(results,q,answer,0)
                assert not record(results,q,answer,0)
            assert summary(results)['score']==600
            assert summary(results)['correct']==30

def test_hints_wrong_and_streak():
    qs=build_adventure(5,'Cambridge Primary','Fractions','Moderate',seed=42)
    results=[]
    record(results,qs[0],qs[0]['answer'],3)
    record(results,qs[1],'-999',0)
    record(results,qs[2],[p['answer'] for p in qs[2]['pairs']],1)
    assert summary(results)['score']==27
    assert summary(results)['best_streak']==1
    assert summary(results)['questions']==3

def test_database_and_pdf(tmp_path,monkeypatch):
    monkeypatch.setenv('MATHQUEST_DB',str(tmp_path/'scores.sqlite3'))
    profile=dict(name='Amy',year=5,syllabus='Cambridge Primary',topic='Fractions',mode='All three levels')
    qs=build_adventure(5,profile['syllabus'],profile['topic'],profile['mode'],seed=99)
    results=[]
    for q in qs:
        record(results,q,[p['answer'] for p in q['pairs']] if q['question_type']=='matching' else q['answer'],0)
    stats=summary(results)
    leaderboard.save('run1',profile,stats);leaderboard.save('run1',profile,stats)
    assert len(leaderboard.rows(profile))==1
    assert not leaderboard.rows(dict(profile,topic='Money'))
    assert create_certificate(profile,results,'run1').startswith(b'%PDF')
