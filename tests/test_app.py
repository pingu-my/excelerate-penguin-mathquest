from streamlit.testing.v1 import AppTest

def test_start_and_numeric_submission(monkeypatch,tmp_path):
    monkeypatch.setenv('MATHQUEST_DB',str(tmp_path/'scores.sqlite3'))
    app=AppTest.from_file('../app.py',default_timeout=15).run()
    assert not app.exception
    app.text_input[0].set_value('Waddle Test')
    app.button[0].click().run()
    assert not app.exception
    q=app.session_state['quest']['questions'][0]
    app.text_input[0].set_value(q['answer'])
    next(b for b in app.button if b.label=='🐧 Submit answer').click().run()
    assert not app.exception
    assert app.session_state['quest']['results'][0]['correct']
    assert len(app.session_state['quest']['results'])==1

def test_complete_mixed_adventure(monkeypatch,tmp_path):
    monkeypatch.setenv('MATHQUEST_DB',str(tmp_path/'scores.sqlite3'))
    app=AppTest.from_file('../app.py',default_timeout=15).run()
    app.text_input[0].set_value('Explorer')
    app.checkbox[0].check()
    app.button[0].click().run()
    for _ in range(10):
        assert not app.exception
        q=app.session_state['quest']['questions'][app.session_state['quest']['index']]
        if q['question_type']=='numeric':app.text_input[0].set_value(q['answer'])
        elif q['question_type']=='mcq':app.radio[0].set_value(q['answer'])
        elif q['question_type']=='matching':
            for widget,pair in zip(app.selectbox,q['pairs']):widget.set_value(pair['answer'])
        next(b for b in app.button if b.label=='🐧 Submit answer').click().run()
        assert not app.exception
        next(b for b in app.button if b.label in ['Next adventure ➜','Finish adventure 🏆']).click().run()
    assert not app.exception
    assert app.session_state['quest']['index']==10
    assert app.session_state['quest']['saved']
    assert len(app.session_state['quest']['results'])==10
