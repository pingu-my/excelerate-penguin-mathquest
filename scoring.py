from curriculum import POINTS
from answer_checker import check_answer

def mark(q, response):
    kind=q['question_type']
    if kind in ['numeric','mcq']:
        return check_answer(response,q['answer'])
    if kind=='matching':
        return len(response)==len(q['pairs']) and all(check_answer(v,p['answer']) for v,p in zip(response,q['pairs']))
    return response==q['answer']

def record(results,q,response,hints):
    """Idempotent marking: the same question cannot increase the score twice."""
    if any(r['id']==q['id'] for r in results):
        return False
    correct=mark(q,response)
    results.append(dict(id=q['id'],difficulty=q['difficulty'],correct=correct,
                        points=POINTS[q['difficulty']][hints] if correct else 0,
                        hints=hints,response=response))
    return True

def summary(results):
    streak=best=0
    for r in results:
        streak=streak+1 if r['correct'] else 0
        best=max(best,streak)
    return dict(score=sum(r['points'] for r in results), correct=sum(r['correct'] for r in results),
                questions=len(results),accuracy=100*sum(r['correct'] for r in results)/len(results) if results else 0,
                streak=streak,best_streak=best)
