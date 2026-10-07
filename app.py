from pathlib import Path
from uuid import uuid4
import csv, io
import streamlit as st
from curriculum import PATHS,DIFFICULTIES,POINTS,available_topics
from question_engine import build_adventure,tex
from answer_checker import number
from scoring import record,summary
from leaderboard import save,rows
from certificate import create_certificate
from components.drag_drop import ordering

st.set_page_config(page_title='EXCELerate Penguin MathQuest',page_icon='🐧',layout='centered')
st.title('🐧 EXCELerate Penguin MathQuest')
st.markdown('**EXCELerate Learning Space** · Learn • Practise • Explore • EXCEL')
st.caption('Waddle is your mathematics adventure guide.')

with st.sidebar:
    st.header('🐧 Waddle’s corner')
    st.write('Use paper for your working. Think carefully before submitting.')
    st.caption('Each question is scored on its first submission. A matching or ordering question earns points only when the whole answer is correct.')
    if st.toggle('🎵 Study music'):
        st.audio(str(Path(__file__).parent/'assets/study_music.wav'),loop=True)
    if 'quest' in st.session_state and st.button('Return to start'):
        del st.session_state.quest
        st.rerun()

if 'quest' not in st.session_state:
    st.subheader('Choose your adventure')
    name=st.text_input('Student first name or nickname',max_chars=50)
    year=st.selectbox('Primary year',[4,5,6])
    syllabus=st.selectbox('Learning path',PATHS)
    topic=st.selectbox('Mathematics topic',available_topics(year,syllabus))
    mode=st.radio('Adventure level',DIFFICULTIES+['All three levels'])
    st.write('10 questions per level · All three levels = 30 questions')
    st.caption('Starter practice uses shared mathematics skills. The learning path is recorded in your results; this version does not claim official curriculum alignment.')
    consent=st.checkbox('Show my nickname and completed result on this app’s leaderboard',value=False)
    if st.button('🚀 Start adventure',type='primary'):
        if not name.strip():st.warning('Enter your first name or nickname to begin.')
        else:
            st.session_state.quest={'run_id':uuid4().hex,'profile':dict(name=name.strip(),year=year,syllabus=syllabus,topic=topic,mode=mode),
              'questions':build_adventure(year,syllabus,topic,mode),'index':0,'results':[],'hints':0,'share':consent,'saved':False}
            st.rerun()
    st.stop()

quest=st.session_state.quest; profile=quest['profile']; stats=summary(quest['results'])
st.subheader(f"Primary {profile['year']} · {profile['topic']}")
c1,c2,c3=st.columns(3)
c1.metric('⭐ Points',stats['score']);c2.metric('✅ Correct',f"{stats['correct']}/{stats['questions']}");c3.metric('🔥 Streak',stats['streak'])
st.progress(quest['index']/len(quest['questions']))

if quest['index']==len(quest['questions']):
    st.success('🏆 Adventure complete! Keep waddling towards excellence!')
    st.write(f"**{stats['correct']}/{stats['questions']} correct · {stats['accuracy']:.1f}% accuracy · {stats['score']} points**")
    st.table([dict(Level=d,**{k:v for k,v in summary([r for r in quest['results'] if r['difficulty']==d]).items() if k in ['score','correct','questions']})
              for d in dict.fromkeys(r['difficulty'] for r in quest['results'])])
    if quest['share'] and not quest['saved']:
        try:
            save(quest['run_id'],profile,stats);quest['saved']=True
        except Exception:
            st.warning('Could not save the leaderboard result. Your certificate is still available. Reload to retry.')
    st.download_button('🎓 Download PDF certificate',create_certificate(profile,quest['results'],quest['run_id']),
                       file_name='EXCELerate_MathQuest_Certificate.pdf',mime='application/pdf')
    output=io.StringIO(); writer=csv.DictWriter(output,fieldnames=['id','difficulty','correct','points','hints','response']);writer.writeheader();writer.writerows(quest['results'])
    st.download_button('Download my question results (CSV)',output.getvalue(),'MathQuest_Results.csv','text/csv')
    with st.expander('Review your questions and solutions'):
        for i,(q,r) in enumerate(zip(quest['questions'],quest['results']),1):
            st.markdown(f"**Question {i} · {q['difficulty']} · {'Correct' if r['correct'] else 'Keep practising'}**")
            st.write(q['instruction'])
            if q['latex']:st.latex(q['latex'])
            if q['question_type'] in ['matching','drag_drop']:
                for p in q.get('pairs',q.get('problems',[])):
                    st.write(p['prompt']);st.latex(p['solution'])
                if q['question_type']=='drag_drop':st.write('Order: '+' → '.join(q['answer']))
            else:st.latex(q['solution'])
    st.subheader('🏆 Waddle’s Hall of Fame')
    st.caption('Completed runs for the same Primary year, learning path, topic and level. Nicknames are self-entered; this is a friendly practice leaderboard.')
    try:
        entries=rows(profile)
        if not entries:st.info('No shared results in this adventure yet.')
        else:
            if quest['saved']:
                rank=next((i for i,r in enumerate(entries,1) if r['run_id']==quest['run_id']),None)
                st.write(f'Your adventure position: #{rank}')
            st.dataframe([{'Rank':i,'Nickname':r['name'],'Points':r['score'],'Correct':f"{r['correct']}/{r['questions']}",'Accuracy':f"{r['accuracy']:.1f}%"} for i,r in enumerate(entries[:10],1)],hide_index=True)
    except Exception:st.warning('Leaderboard is currently unavailable.')
    if st.button('🔄 Start a new adventure'):
        del st.session_state.quest;st.rerun()
    st.stop()

q=quest['questions'][quest['index']];key=f"{quest['run_id']}_{q['id']}"
answered=len(quest['results'])>quest['index']
st.markdown(f"### Question {quest['index']+1}/{len(quest['questions'])} · {q['difficulty']}")
st.caption(f"{q['question_type'].replace('_',' ').title()} · Up to {POINTS[q['difficulty']][0]} points")
st.write(q['instruction'])
if q['latex']:st.latex(q['latex'])
response=None
if not answered:
    if q['question_type']=='numeric':
        response=st.text_input('Your answer',key=key,placeholder='e.g. 20, 0.5, 1/2, 1 1/2 or 50%')
        st.caption('Use the units in the question; type the number only. Fractions and exact equivalent decimals or percentages are accepted. Do not round unless asked.')
    elif q['question_type']=='mcq':
        response=st.radio('Choose one answer',q['options'],index=None,format_func=lambda x:f'${tex(x)}$',key=key)
    elif q['question_type']=='matching':
        response=[]
        for i,p in enumerate(q['pairs']):
            st.write(f"**{chr(65+i)}.** {p['prompt']}")
            if p['latex']:st.latex(p['latex'])
            response.append(st.selectbox('Choose the matching answer',q['options'],index=None,
              format_func=lambda x:f'${tex(x)}$',key=f'{key}_match_{i}'))
    else:
        for p in q['problems']:
            st.write(f"**{p['label']}.** {p['prompt']}")
            if p['latex']:st.latex(p['latex'])
        response=ordering(q['cards'],key)
    if quest['hints']<3 and st.button(f"💡 Ask Waddle for hint {quest['hints']+1}",key=key+'_hint'):
        quest['hints']+=1;st.rerun()
    for hint in q['hints'][:quest['hints']]:st.info('🐧 '+hint)
    st.caption(f"Correct answer now earns {POINTS[q['difficulty']][quest['hints']]} points.")
    if st.button('🐧 Submit answer',type='primary',key=key+'_submit'):
        complete=response is not None and response!='' and (not isinstance(response,list) or all(v is not None for v in response))
        if q['question_type']=='numeric' and complete:
            try:number(response)
            except (ValueError,ZeroDivisionError):
                complete=False;st.warning('Use a valid number or fraction, without units. A fraction cannot have zero as its denominator.')
        if not complete:st.warning('Complete your answer before submitting.')
        else:
            record(quest['results'],q,response,quest['hints']);st.rerun()
else:
    result=quest['results'][quest['index']]
    if result['correct']:st.success(f"🎉 Waddle-tastic! +{result['points']} points!")
    else:st.info('🐧 Good effort. Study the solution, then try the next problem.')
    st.write('Your submitted answer:',str(result['response']))
    st.markdown('**Solution**')
    if q['question_type'] in ['matching','drag_drop']:
        for p in q.get('pairs',q.get('problems',[])):st.latex(p['solution'])
        if q['question_type']=='drag_drop':st.write('Correct order: '+' → '.join(q['answer']))
    else:st.latex(q['solution'])
    if st.button('Finish adventure 🏆' if quest['index']+1==len(quest['questions']) else 'Next adventure ➜',type='primary',key=key+'_next'):
        quest['index']+=1;quest['hints']=0;st.rerun()
