/**
 * @fileoverview CriticalRoutesService.gs
 * @description Implements functions to analyze critical routes, e.g., identifying routes with high occupancy.
 */

/**
 * Analyzes routes to identify those with high occupancy based on student count and bus capacity.
 * @returns {Array<object>} A list of critical routes with their current occupancy and capacity.
 */
function analyzeCriticalRoutes() {
    const allRoutes = getByEntity("Rota");
    const allOnibus = getByEntity("Onibus");
    const allAlunos = getByEntity("Aluno");

    const onibusMap = new Map(allOnibus.map(bus => [bus.Modelo, bus.Capacidade]));
    const routeOccupancy = {};

    allAlunos.forEach(aluno => {
        if (aluno.Ativo === true || aluno.Ativo === "TRUE") { // Assuming 'Ativo' is a boolean or string 'TRUE'/'FALSE'
            if (routeOccupancy[aluno.Rota]) {
                routeOccupancy[aluno.Rota]++;
            } else {
                routeOccupancy[aluno.Rota] = 1;
            }
        }
    });

    const criticalRoutes = [];

    allRoutes.forEach(route => {
        const currentOccupancy = routeOccupancy[route.Nome] || 0;
        const busCapacity = onibusMap.get(route.Onibus) || 0; // Assuming route.Onibus stores the bus Model

        if (busCapacity > 0 && currentOccupancy / busCapacity > 0.8) { // Example: over 80% capacity
            criticalRoutes.push({
                Nome: route.Nome,
                Descricao: route.Descricao,
                Onibus: route.Onibus,
                CapacidadeOnibus: busCapacity,
                OcupacaoAtual: currentOccupancy,
                PercentualOcupacao: ((currentOccupancy / busCapacity) * 100).toFixed(2) + 
'%'
            });
        }
    });

    return criticalRoutes;
}


