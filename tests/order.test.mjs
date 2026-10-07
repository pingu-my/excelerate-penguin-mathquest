// Small interaction test; no browser dependency is required.
import fs from 'node:fs';
import assert from 'node:assert/strict';
class Element {
  constructor(tag){this.tag=tag;this.children=[];this.classList={add(){},remove(){}};}
  append(node){this.children.push(node)}
  replaceChildren(){this.children=[]}
  setAttribute(){}
}
const board=new Element('div');
globalThis.document={createElement:tag=>new Element(tag)};
const source=fs.readFileSync(new URL('../components/order.js',import.meta.url),'utf8');
const {default: render}=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
let value;
render({parentElement:{querySelector:()=>board},data:{order:['C','A','B']},setStateValue:(key,v)=>{assert.equal(key,'order');value=v}});
board.children[1].children[2].onclick(); // Move C down.
assert.deepEqual(value,['A','C','B']);
board.children[3].ondragstart({dataTransfer:{setData(){}}});
board.children[1].ondrop({preventDefault(){}}); // Move B to the top.
assert.deepEqual(value,['B','A','C']);
console.log('Ordering buttons and drag/drop state test passed.');
