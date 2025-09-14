/**
 * @fileoverview SchemaService.gs
 * @description Single source of truth for the application's data contract.
 * This service centralizes all sheet names, headers, data types, and validation rules,
 * making the application robust and easier to maintain.
 */

const SHEET_NAMES = {
    ALUNOS: 'Alunos',
    ROTAS: 'Rotas',
    ONIBUS: 'Onibus',
    MONITORES: 'Monitores',
    SECRETARIOS: 'Secretários',
    ESCOLAS: 'Escolas',
    PAIS: 'Pais',
    PONTOS_DE_PARADA: 'Pontos de Parada',
    OCORRENCIAS: 'Ocorrências',
    FREQUENCIA: 'Frequência',
    ALUNOS_HISTORY: 'Alunos_History',
    ROTAS_HISTORY: 'Rotas_History',
    ONIBUS_HISTORY: 'Onibus_History',
    // Add other history sheets as needed
};

const SCHEMAS = {
    Aluno: {
        fields: {
            ID: { type: 'number', readonly: true, label: 'ID' },
            Nome: { type: 'string', required: true, label: 'Nome do Aluno' },
            CPF: { type: 'cpf', required: true, label: 'CPF' },
            DataNascimento: { type: 'date', required: true, label: 'Data de Nascimento' },
            Escola: { type: 'string', required: true, label: 'Escola' },
            Turno: { type: 'string', required: true, label: 'Turno' },
            Endereco: { type: 'string', required: true, label: 'Endereço' },
            PontoDeParada: { type: 'string', required: true, label: 'Ponto de Parada' },
            Rota: { type: 'string', required: true, label: 'Rota' },
            Onibus: { type: 'string', required: true, label: 'Ônibus' },
            Monitor: { type: 'string', required: true, label: 'Monitor' },
            Telefone: { type: 'phone', required: true, label: 'Telefone' },
            Email: { type: 'email', required: false, label: 'Email' },
            Ativo: { type: 'boolean', defaultValue: true, label: 'Ativo' },
        }
    },
    Rota: {
        fields: {
            ID: { type: 'number', readonly: true, label: 'ID' },
            Nome: { type: 'string', required: true, label: 'Nome da Rota' },
            Descricao: { type: 'string', required: false, label: 'Descrição' },
            Onibus: { type: 'string', required: true, label: 'Ônibus' },
            Monitor: { type: 'string', required: true, label: 'Monitor' },
            HorarioPartida: { type: 'string', required: true, label: 'Horário de Partida' },
            HorarioChegada: { type: 'string', required: true, label: 'Horário de Chegada' },
            Ativo: { type: 'boolean', defaultValue: true, label: 'Ativo' },
        }
    },
    Onibus: {
        fields: {
            ID: { type: 'number', readonly: true, label: 'ID' },
            Placa: { type: 'string', required: true, label: 'Placa' },
            Modelo: { type: 'string', required: true, label: 'Modelo' },
            Capacidade: { type: 'number', required: true, label: 'Capacidade' },
            Ano: { type: 'number', required: true, label: 'Ano' },
            Ativo: { type: 'boolean', defaultValue: true, label: 'Ativo' },
        }
    },
    // Add other schemas as needed
};

const ENTITY_TO_SHEET = {
    Aluno: SHEET_NAMES.ALUNOS,
    Rota: SHEET_NAMES.ROTAS,
    Onibus: SHEET_NAMES.ONIBUS,
    // Add other mappings as needed
};

const FIELD_ALIASES = {
    Aluno: {
        CPF: 'CPF_Aluno',
    },
    // Add other aliases as needed
};

function getSchema(entityName) {
    return SCHEMAS[entityName];
}

function getSheetName(entityName) {
    return ENTITY_TO_SHEET[entityName];
}

function getSheetHeaders(sheetKey) {
    const entityName = Object.keys(ENTITY_TO_SHEET).find(key => ENTITY_TO_SHEET[key] === sheetKey);
    if (entityName) {
        const schema = getSchema(entityName);
        const aliases = FIELD_ALIASES[entityName] || {};
        return Object.keys(schema.fields).map(field => aliases[field] || field);
    }
    return [];
}


