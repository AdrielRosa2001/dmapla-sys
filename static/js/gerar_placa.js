function cancel(){
    document.getElementById('input_item').style.display = 'none';
}
function showInputItem(bloco){
    console.log(bloco)
    document.getElementById('codigo-produto').value = '';
    document.getElementById('number-block').innerHTML = bloco;
    document.getElementById('input_item').style.display = 'block';
    document.getElementById('codigo-produto').value = '';
    $("#codigo-produto").focus();
}
function setItemBlock(){
    const bloco = document.getElementById('number-block').innerHTML;
    const code = document.getElementById('codigo-produto').value;
    document.getElementById(`title-block-${bloco}`).innerHTML = code;
    document.getElementById(`title-block-${bloco}`).style.display = 'block';
    document.getElementById(`add-btn-${bloco}`).style.display = 'none';
    document.getElementById(`rmv-btn-${bloco}`).style.display = 'block';
    cancel()
}
function removeCode(bloco){
    document.getElementById(`title-block-${bloco}`).innerHTML = "";
    document.getElementById(`title-block-${bloco}`).style.display = 'none';
    document.getElementById(`rmv-btn-${bloco}`).style.display = 'none';
    document.getElementById(`add-btn-${bloco}`).style.display = 'block';

}
function gerarPagina(){
    loadEnabled();
    var list = [];
    for (var i = 1 ; i <= 10 ; i++){
        var code = document.getElementById(`title-block-${i}`).innerHTML;
        if ( code.length <= 13) {
            list.push(code)
        }
    }
    if (list.length != 0){
        enviarDados(list)
        limparPagina()
    } else{
        console.log('Nenhum codigo detectado!')
    }
}
function limparPagina(){
    for (var i = 1 ; i <= 10 ; i++){
        removeCode(i);
    }
}
function enviarDados(array_list){
    document.getElementById('lista').value = "";
    document.getElementById('lista').value = array_list;
    document.getElementById('send_lista').click();
}
