# Proposta de Sistema Integrado de Gestão de Transporte Escolar (SIG-TE)

## 1. Introdução

Esta proposta detalha a concepção de um Sistema Integrado de Gestão de Transporte Escolar (SIG-TE), combinando e harmonizando funcionalidades identificadas nos documentos `SIG-TE.txt` e `pasted_content.txt`. O objetivo principal é desenvolver uma plataforma robusta, segura e escalável, com foco na otimização de custos operacionais e na melhoria da experiência do usuário e da gestão.

O sistema proposto adota uma arquitetura 


puramente serverless, conforme preconizado em `pasted_content.txt`, utilizando Google Apps Script para o backend, Google Sheets como base de dados principal e APIs do Google Cloud (Maps, Gemini) para funcionalidades avançadas. Este modelo visa um custo operacional próximo de zero, escalabilidade inerente e alta manutenibilidade.

## 2. Visão Geral da Arquitetura

A arquitetura do SIG-TE será fundamentada em um stack serverless, aproveitando o ecossistema do Google Cloud e Google Workspace. A escolha por essa abordagem se justifica pela necessidade de minimizar custos ociosos e garantir escalabilidade automática. Os principais pilares arquiteturais são:

*   **Frontend (SPA):** Uma Single-Page Application (SPA) moderna e responsiva, desenvolvida com HTML, CSS e JavaScript, será o ponto de interação do usuário. Esta SPA se comunicará com o backend via `google.script.run`, garantindo uma experiência fluida e sem recarregamento de página.
*   **Backend (Google Apps Script):** Toda a lógica de negócio e integração com os serviços do Google será implementada em Google Apps Script. Este ambiente serverless permite a execução de funções sob demanda, sem a necessidade de gerenciar servidores.
*   **Base de Dados (Google Sheets):** As planilhas do Google Sheets atuarão como a camada de persistência de dados. A simplicidade e a familiaridade com o Sheets, combinadas com a capacidade de serem acessadas e manipuladas via Apps Script, tornam-no uma solução de baixo custo e fácil gerenciamento para dados estruturados.
*   **APIs do Google Cloud:** Para funcionalidades que exigem processamento mais intensivo ou recursos específicos, como geocodificação, otimização de rotas e inteligência artificial, serão utilizadas as APIs do Google Maps e do Google Gemini, acessadas via Apps Script. O modelo pay-per-use dessas APIs alinha-se ao princípio de custo zero ocioso.
*   **Segurança (Google Identity):** A autenticação e autorização serão gerenciadas através do Google Identity (OAuth2), garantindo um modelo de segurança robusto e familiar aos usuários do Google Workspace. O controle de acesso baseado em funções (RBAC) será implementado na camada de aplicação.

Esta arquitetura permite um desenvolvimento ágil, implantação simplificada e um ambiente operacional eficiente, alinhado com a visão de um sistema de 


alto padrão e baixo custo operacional.

## 3. Componentes Essenciais e Harmonização

A seguir, detalhamos os componentes essenciais do SIG-TE, sua funcionalidade e como eles são harmonizados para criar um sistema coeso e eficiente, integrando as melhores práticas e funcionalidades de ambos os documentos de referência.

### 3.1. `appsscript.json` Manifest

O arquivo `appsscript.json` é a espinha dorsal da configuração do projeto Google Apps Script. Ele define as permissões necessárias (OAuth scopes), o ambiente de execução e os níveis de acesso da aplicação web. A configuração proposta, conforme `pasted_content.txt`, incluirá os seguintes scopes para garantir a interoperabilidade com os serviços do Google:

```json
{
  "timeZone": "America/Sao_Paulo",
  "runtimeVersion": "V8",
  "exceptionLogging": "STACKDRIVER",
  "oauthScopes": [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/script.external_request",
    "https://www.googleapis.com/auth/script.scriptapp",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/forms"
  ],
  "webapp": {
    "access": "ANYONE",
    "executeAs": "USER_DEPLOYING"
  }
}
```

Este manifest garante que a aplicação tenha as permissões adequadas para interagir com o Google Sheets (base de dados), Google Drive (para possível armazenamento de documentos), realizar requisições externas (para APIs do Google Maps e Gemini) e obter informações básicas do usuário para autenticação. A execução como `USER_DEPLOYING` simplifica o gerenciamento de permissões para o desenvolvedor.

### 3.2. Gerenciamento de Dados: `SchemaService.gs`, `DataManager.gs` e `ValidationService.gs`

O gerenciamento de dados é central para qualquer sistema, e no SIG-TE, ele será robusto e modular. A abordagem de `pasted_content.txt` é adotada por sua clareza e manutenibilidade, abstraindo a complexidade do Google Sheets como base de dados.

*   **`SchemaService.gs` (Master Schema Service):** Este serviço atua como a fonte única de verdade para o contrato de dados da aplicação. Ele centraliza todos os nomes das planilhas (`SHEET_NAMES`), os cabeçalhos esperados, os tipos de dados de cada campo e as regras de validação. Isso garante consistência e facilita a manutenção, pois qualquer alteração na estrutura dos dados é refletida em um único local. Inclui mapeamentos lógicos (`ENTITY_TO_SHEET`) e de campos (`FIELD_ALIASES`) para flexibilidade.

*   **`DataManager.gs` (Generic CRUD Service):** Este componente é responsável por todas as operações de Create, Read, Update e Delete (CRUD) com as planilhas do Google Sheets. Ele utiliza o `SchemaService.gs` para entender a estrutura dos dados, realizar mapeamento de cabeçalhos e conversões de tipo. As funcionalidades incluem `getByEntity` (com filtragem, ordenação e paginação), `getById`, `create`, `update` e `delete` (implementando *soft delete*). Uma característica crucial é o **History Tracking**, que registra automaticamente as alterações em planilhas de histórico (`[SheetName]_History`), mantendo um rastro de auditoria das modificações, quem as fez e quando. Isso harmoniza a necessidade de persistência de dados com a rastreabilidade, um aspecto implícito na classe `DB` de `SIG-TE.txt`.

*   **`ValidationService.gs`:** Garante a integridade dos dados antes que sejam escritos nas planilhas. Ele valida os objetos de dados contra os esquemas definidos no `SchemaService.gs`, aplicando regras de validação para tipos como `string`, `number`, `date`, `boolean`, e validadores específicos para formatos brasileiros como CPF, telefone e e-mail. Este serviço é invocado pelo `DataManager.gs` antes de qualquer operação de escrita, prevenindo dados inconsistentes.

Essa tríade de serviços substitui e aprimora a classe `DB` encontrada em `SIG-TE.txt`. Embora a classe `DB` ofereça um sistema de *locking* mais explícito, a abordagem modular proposta é mais alinhada com o ambiente serverless do Apps Script e mais fácil de escalar e manter. O *locking* pode ser incorporado ao `DataManager.gs` em futuras iterações, se a concorrência se tornar um problema crítico.

### 3.3. Autenticação e Autorização: `AuthService.gs`

A segurança é um pilar fundamental do SIG-TE. O `AuthService.gs` centraliza a gestão de autenticação e permissões, utilizando o Google Identity para um processo seguro e familiar aos usuários.

*   **Autenticação:** A função `authenticate(googleToken)` verificará um token de ID do Google (simulado no Apps Script pela obtenção do e-mail do usuário ativo, mas em produção envolveria a validação real do token com a API do Google). Após a verificação, o serviço consultará as planilhas de `Secretários` e `Monitores` para atribuir papéis ao usuário, definindo seu nível de acesso no sistema.

*   **Autorização:** A função `hasPermission(user, requiredPermission)` implementa o controle de acesso baseado em funções (RBAC). Com base nos papéis atribuídos ao usuário, ela determinará se ele possui a permissão necessária para executar uma determinada ação (ex: `manage_alunos`, `view_rotas`). Isso garante que apenas usuários autorizados possam acessar e modificar dados sensíveis.

Esta abordagem formaliza e centraliza a lógica de segurança que estava mais dispersa em `SIG-TE.txt`, oferecendo um modelo mais robusto e fácil de gerenciar.

### 3.4. Otimização de Rotas e Mapas: `GoogleMapsService.gs` e `CriticalRoutesService.gs`

As funcionalidades de otimização de rotas são cruciais para um sistema de transporte escolar. O `GoogleMapsService.gs` encapsula a interação com a API do Google Maps, enquanto o `CriticalRoutesService.gs` aplica essa capacidade para análises de negócio específicas.

*   **`GoogleMapsService.gs`:** Este serviço atua como um wrapper para a API do Google Maps. Ele gerencia a chave de API (obtida de Script Properties) e fornece funções para:
    *   `geocodeAddress(address)`: Converte um endereço em coordenadas geográficas.
    *   `optimizeRoute(origin, destination, waypoints)`: Otimiza uma rota, retornando detalhes como distância, duração e a ordem otimizada dos waypoints. Esta função é uma implementação direta e aprimorada da `optimizeRoute()` de `SIG-TE.txt`.
    *   `buildGoogleMapUrl(origin, destination, waypoints, optimizedOrder)`: Constrói uma URL para visualização da rota otimizada no Google Maps, similar à função de mesmo nome em `SIG-TE.txt`.

*   **`CriticalRoutesService.gs`:** Este serviço de negócio utiliza as capacidades do `GoogleMapsService.gs` e do `DataManager.gs` para identificar rotas com alta ocupação. A função `analyzeCriticalRoutes()` buscará dados de alunos, ônibus e rotas para calcular a ocupação percentual e sinalizar rotas que excedem um determinado limite (ex: 80% da capacidade do ônibus). Isso transforma uma funcionalidade de utilidade (otimização de rota) em uma ferramenta de inteligência de negócio, ajudando na tomada de decisões e na gestão da frota.

### 3.5. Inteligência Artificial e Relatórios: `GeminiService.gs` e `GeminiReportService.gs`

Uma das inovações propostas em `pasted_content.txt` é a integração de capacidades de IA, que não estavam presentes em `SIG-TE.txt`. Isso adiciona uma camada de inteligência e automação ao sistema.

*   **`GeminiService.gs`:** Este é um wrapper de baixo nível para a API Gemini 2.5 Flash. Ele gerencia a chave de API (também de Script Properties), constrói as requisições para a API do Gemini e faz o parsing das respostas. Um aspecto importante é a inclusão de **caching** (`CacheService`) para reduzir custos e melhorar a performance, evitando chamadas repetidas para o mesmo prompt.

*   **`GeminiReportService.gs`:** Utiliza o `GeminiService.gs` para gerar relatórios e análises inteligentes. A função `generateDiagnosticReport()` coleta dados de outros serviços (como `CriticalRoutesService.gs` e `AbsenceAnalysisService.gs`) e constrói um prompt detalhado para o Gemini, que então sintetiza um relatório diagnóstico com análises e sugestões. Outra função, `generateEntitySummary(entityName, id)`, pode gerar resumos concisos de registros específicos. Isso eleva o sistema de um mero gerenciador de dados para uma ferramenta de apoio à decisão.

### 3.6. Análise de Padrões de Ausência: `AbsenceAnalysisService.gs`

Complementando as funcionalidades de IA, o `AbsenceAnalysisService.gs` é projetado para identificar proativamente alunos em risco devido a padrões de ausência. Embora atualmente seja um *placeholder*, sua estrutura prevê a integração com uma futura planilha de `Frequência` para:

*   Analisar dados de frequência.
*   Definir critérios para alunos em risco (ex: X faltas consecutivas, Y faltas em um período).
*   Identificar e listar alunos que se enquadram nesses critérios.

Esta funcionalidade, introduzida em `pasted_content.txt`, é vital para a gestão proativa do bem-estar dos alunos e a otimização do transporte.

### 3.7. Notificações: `NotificationService.gs`

O `NotificationService.gs` centraliza a lógica de envio de notificações, generalizando o conceito de comunicação que aparece de forma pontual em `SIG-TE.txt` (ex: `sendReauthorizationRequest`).

*   **`createNotification(type, message, recipient, details)`:** Uma função genérica para criar e enviar notificações. Pode ser configurada para enviar e-mails (usando `MailApp`), registrar em uma planilha de `Notificações`, ou integrar com outros sistemas de alerta. Isso permite que diferentes partes do sistema (ex: `AbsenceAnalysisService`, `GeminiReportService`) enviem alertas de forma consistente.
*   **`checkPendingAttestations()`:** Um *placeholder* para uma funcionalidade futura que verificaria atestados pendentes e enviaria lembretes ou alertas, garantindo que processos administrativos importantes não sejam negligenciados.

### 3.8. Agendamento de Tarefas

Ambos os documentos reconhecem a necessidade de tarefas automatizadas. A proposta integra a funcionalidade de agendamento de `SIG-TE.txt` com os novos serviços.

*   **`adjustScheduleTrigger()` e `respondToHourlyTrigger()`:** As funções de `SIG-TE.txt` para gerenciar triggers baseados em tempo serão mantidas. No entanto, a `respondToHourlyTrigger()` será adaptada para invocar os novos serviços, como `generateDiagnosticReport()` do `GeminiReportService.gs` ou `checkPendingAttestations()` do `NotificationService.gs`, garantindo que análises e alertas proativos sejam executados regularmente. A configuração desses triggers será detalhada no `README.md`.

### 3.9. Frontend (SPA): `index.html`, `styles.css`, `main.js`

A experiência do usuário é prioridade, e a arquitetura de Single-Page Application (SPA) proposta em `pasted_content.txt` oferece uma interface moderna e responsiva, superando a abordagem de múltiplos arquivos HTML e diálogos de `SIG-TE.txt`.

*   **`index.html`:** O ponto de entrada da SPA, fornecendo a estrutura HTML básica com placeholders para cabeçalho, navegação lateral (collapsible sidebar), área de conteúdo principal (onde as seções serão renderizadas dinamicamente) e modais. Ele carregará `styles.css` e `main.js`.

*   **`styles.css`:** Um stylesheet profissional e responsivo, utilizando variáveis CSS para facilitar a tematização. Ele garantirá uma identidade visual consistente e de "alto padrão corporativo", conforme a visão do projeto.

*   **`main.js`:** O coração do frontend, gerenciando a lógica da SPA:
    *   **Router:** Um roteador simples baseado em hash (`#/dashboard`, `#/alunos`) para navegação sem recarregamento de página.
    *   **API Client:** Um wrapper para `google.script.run`, facilitando a comunicação com os serviços backend do Apps Script, incluindo tratamento de erros e indicadores de carregamento.
    *   **UI Manager:** Funções para controlar estados de carregamento, exibir notificações e gerenciar modais.
    *   **Dynamic Rendering:** Funções como `renderDashboard`, `renderDataTable` (com ordenação e paginação client-side) e `renderForm` (que constrói formulários dinamicamente a partir do `SchemaService.gs`) garantirão uma interface interativa e adaptável. As funcionalidades de UI de `SIG-TE.txt` (como `openDialog`, `openAboutSidebar`) serão reimplementadas como componentes ou seções dentro desta SPA.

Essa arquitetura de frontend proporciona uma experiência de usuário superior, mais fluida e moderna, alinhada com as expectativas de um SaaS de alta qualidade.




## 4. Implantação

A implantação do SIG-TE seguirá um processo claro e documentado, garantindo que o sistema possa ser configurado e atualizado de forma eficiente. As instruções detalhadas serão fornecidas em um arquivo `README.md`, conforme sugerido em `pasted_content.txt`.

### 4.1. `README.md` (Instruções de Implantação)

O `README.md` será o guia definitivo para a implantação e configuração do sistema, cobrindo os seguintes pontos:

*   **Pré-requisitos:** Instalação do `clasp` (ferramenta de linha de comando para Google Apps Script).
*   **Configuração do Projeto:**
    *   Clonagem do repositório do código-fonte.
    *   Autenticação com o Google via `clasp login`.
    *   Criação de um novo projeto Apps Script ou upload dos arquivos para um projeto existente usando `clasp create` ou `clasp push`.
*   **Configuração de Propriedades de Script:** Instruções claras sobre como definir as chaves de API necessárias (ex: `GEMINI_API_KEY`, `GOOGLE_MAPS_API_KEY`) nas Propriedades de Script do projeto Apps Script. Isso garante que informações sensíveis não sejam codificadas diretamente no código-fonte.
*   **Configuração do Google Sheet:** Detalhes 
(Content truncated due to size limit. Use page ranges or line ranges to read remaining content)