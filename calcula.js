const data = new Date();
const dataInicial = '01/01/2025';

const mesAnterior = new Date(data);
mesAnterior.setMonth(data.getMonth() - 1);

let dataBR = mesAnterior.toLocaleDateString("pt-BR", { dateStyle: "short" });

const dataFinal = dataBR;
console.log(dataFinal);

const url = `https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json&dataInicial=01/${dataInicial}&dataFinal=${dataFinal}`;

fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Somar os valores da taxa SELIC
        const somaSelic = data.reduce((soma, item) => {
            const valor = parseFloat(item.valor.replace(',', '.'));
            return soma + valor;
        }, 0);

        console.log(`Soma dos valores da SELIC: ${somaSelic}%`);
    })
    .catch(error => {
        console.error('Erro ao buscar dados:', error);
    });
