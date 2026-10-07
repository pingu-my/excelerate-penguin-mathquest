export default function({parentElement, data, setStateValue}) {
  const root = parentElement.querySelector('.board');
  let order = [...data.order], dragged = null;
  const move = (from,to) => {
    if(from===to || from<0 || to<0 || to>=order.length) return;
    const [item]=order.splice(from,1); order.splice(to,0,item);
    render(); setStateValue('order',[...order]);
  };
  function render() {
    root.replaceChildren();
    const help=document.createElement('small');
    help.textContent='Smallest → largest. Drag cards, or use the ↑ and ↓ buttons on phones and keyboards.';
    root.append(help);
    order.forEach((label,index)=>{
      const card=document.createElement('div'); card.className='card'; card.draggable=true;
      const title=document.createElement('span');title.textContent=`${index+1}. Problem ${label}`;card.append(title);
      ['↑','↓'].forEach((symbol,i)=>{
        const button=document.createElement('button');button.textContent=symbol;
        button.setAttribute('aria-label',`Move problem ${label} ${i===0?'up':'down'}`);
        button.disabled=i===0?index===0:index===order.length-1;
        button.onclick=()=>move(index,index+(i===0?-1:1));card.append(button);
      });
      card.ondragstart=e=>{dragged=index;e.dataTransfer.setData('text/plain',label);card.classList.add('dragging')};
      card.ondragend=()=>card.classList.remove('dragging');
      card.ondragover=e=>e.preventDefault();
      card.ondrop=e=>{e.preventDefault();if(dragged!==null)move(dragged,index);dragged=null};
      root.append(card);
    });
  }
  render();
}
