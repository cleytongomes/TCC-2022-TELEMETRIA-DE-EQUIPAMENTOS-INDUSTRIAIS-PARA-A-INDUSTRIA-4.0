// Jquery
$(document).ready(function() {

    // Objeto js com os identificadores das maquinas e nomes
    var maquinas = {};
    
    // Carrega as máquinas
    $.ajax({
        url: 'http://localhost:5000/estados_maquinas',
        type: 'GET',
        dataType: 'json',
        success: function(data) {

            // Percorre as máquinas
            for (let i = 0; i < data.length; i++) {

                console.log(data[i]);

                let identificador = data[i][1];
                let nome = data[i][2];

                let ultimo_estado = data[i][3];
                let finalizada = data[i][4];

                // Adiciona a máquina no objeto
                maquinas[identificador] = nome;

                // Cria o elemento html
                let html_estado_atual =  '';
                if (finalizada) {
                    html_estado_atual = '<span class="badge badge-secondary">Desconhecido</span>';
                }else{
                    if (ultimo_estado == "LIGADA") {
                        html_estado_atual = '<span class="badge badge-success">Em Trabalho</span>';
                    }else if (ultimo_estado == "DESLIGADA") {
                        html_estado_atual = '<span class="badge badge-danger">Parada</span>';
                    }
                }

                var html =  '<div id="' + identificador + '" class="card mt-5">' +
                                '<div class="card-header">' +
                                    '<h3>' + nome + '</h3>' +
                                '</div>' +
                                '<div class="card-body">' +
                                    '<div class="row">' +
                                        '<div class="col-12 col-md-6">' +
                                            '<canvas id="chart_' + identificador + '" width="400" ></canvas>' +
                                        '</div>' +
                                        '<div class="col-12 col-md-6">' +
                                            '<h3>Status</h3>' +
                                            '<p class="estado_atual">' +
                                                html_estado_atual +
                                            '</p>' +
                                            '<br>' +
                                            '<h3>Tempo em Trabalho</h3>' +
                                            '<p>' +
                                                '<span class="badge badge-success tempo-trabalho">00:00:00</span>' +
                                            '</p>' +
                                            '<h3>Tempo em Parada</h3>' +
                                            '<p>' +
                                                '<span class="badge badge-success tempo-parada">00:00:00</span>' +
                                            '</p>' +
                                        '</div>' +
                                    '</div>' +
                                '</div>' +
                            '</div>';
                
                // Insere o html na página
                $('#maquinas').append(html);

            }

            // Carrega os dados das máquinas
            carregarDadosMaquinas();
        }
    });

    // Carrega os dados das máquinas
    function carregarDadosMaquinas() {            
        // Percorre as máquinas
        for (let i = 0; i < Object.keys(maquinas).length; i++) {

            let identificador = Object.keys(maquinas)[i];

            // Carrega os dados da máquina
            $.ajax({
                url: 'http://localhost:5000/maquina/' + identificador,
                type: 'GET',
                dataType: 'json',
                success: function(data) {

                    let tempo_ligada = 0;
                    let tempo_desligada = 0;

                    // Percorre os dados
                    for (let i = 0; i < data.length; i++) {
                        if (data[i][0] == 'LIGADA') {
                            tempo_ligada += parseInt(data[i][1]);
                        } else {
                            tempo_desligada += parseInt(data[i][1]);
                        }
                    }

                    // Atualiza os dados
                    $('#' + identificador + ' .tempo-trabalho').html(tempo_ligada + ' Horas');
                    $('#' + identificador + ' .tempo-parada').html(tempo_desligada + ' Horas');

                    // Cria o gráfico
                    carregarGrafico(identificador, tempo_ligada, tempo_desligada);

                }
            });
        }
    }

    // Carrega o gráfico
    function carregarGrafico(identificador, Ligada, Desligada) {
        var labels = ["Em Trabalho", "Parada"];
        var valores = [Ligada, Desligada];
        var barColors = [
            "#00aba9",
            "#b91d47",
        ];

        new Chart("chart_" + identificador, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    backgroundColor: barColors,
                    data: valores
                }]
            },
            options: {
                title: {
                    display: true,
                    text: "Tempo Trabalho x Tempo Parada"
                }
            }
        });
    }

});
