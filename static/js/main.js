var idade = "";
var reg = /^\d+$/;

$(document).click(function(event) {
    var valor = $(event.target).text();

    if(valor == "ok"){
        $("#bloco-sexo").focus();
    }

    if(reg.test(valor)){
        idade = idade + '' + valor;
        $(".valor-idade").html(idade);
    }
});

function limparIdade(){
    $(".valor-idade").html("");
        idade = "";
}

/* COMPONENTE DE RADIO BUTTON*/
const st = {};

st.flap = document.querySelector('#flap');
st.toggle = document.querySelector('.toggle');

st.choice1 = document.querySelector('#choice1');
st.choice2 = document.querySelector('#choice2');

st.flap.addEventListener('transitionend', () => {

    if (st.choice1.checked) {
        st.toggle.style.transform = 'rotateY(-15deg)';
        setTimeout(() => st.toggle.style.transform = '', 400);
    } else {
        st.toggle.style.transform = 'rotateY(15deg)';
        setTimeout(() => st.toggle.style.transform = '', 400);
    }

})

st.clickHandler = (e) => {

    if (e.target.tagName === 'LABEL') {
        setTimeout(() => {
            st.flap.children[0].textContent = e.target.textContent;
        }, 250);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    st.flap.children[0].textContent = st.choice2.nextElementSibling.textContent;
});

document.addEventListener('click', (e) => st.clickHandler(e));
/* COMPONENTE DE RADIO BUTTON*/