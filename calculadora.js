const data = new Date();
const dataInicial = '01/01/2025';

const mesAnterior = new Date(data);
mesAnterior.setMonth(data.getMonth() - 1);

let dataBR = mesAnterior.toLocaleDateString("pt-BR", { dateStyle: "short" });

const dataFinal = dataBR;
console.log(dataFinal);

const url = `https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json&dataInicial=${dataInicial}&dataFinal=${dataFinal}`;

fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Somar os valores da taxa SELIC
        const somaSelic = data.reduce((soma, item) => {const valor = parseFloat(item.valor.replace(',', '.'));
            return soma + valor;
        }, 0);

        console.log(`Soma dos valores da SELIC: ${somaSelic}%`);
        return somaSelic;

    })
    .catch(error => {
        console.error('Erro ao buscar dados:', error);
    });

function calcular_valor_cedivel(valor_bruto, somaSelic, percentual_honorario, rra=0.03) {
    // Faz o calculo da Selic e soma com o valor bruto
    var selic_valor = valor_bruto * (somaSelic / 100)
    var valor_liquido = valor_bruto + selic_valor

    // Desconta o valor do RRA e o percentual do honorário
    var valor_rra = valor_liquido * rra
    var valor_recebido = valor_liquido - (valor_liquido * (percentual_honorario / 100)) - valor_rra

    // Retorna o valor final arredondado
    return valor_recebido
}

console.log(`Valor cedivel ${calcular_valor_cedivel(200000, 1.92, 30)}`)