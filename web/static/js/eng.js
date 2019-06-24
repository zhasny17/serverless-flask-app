var p = document.getElementsByClassName('aux');
var newElem  = document.createElement('p');
var text     = document.createTextNode('Connected!...');
newElem.appendChild(text);
p.insertBefore(newElem);
setTimeout(function () {
    console.log('testing...')
}, 10);