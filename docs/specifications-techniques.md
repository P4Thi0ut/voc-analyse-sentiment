Keyword Extraction Feature Implementation
Overview
Implement a keyword extraction feature following the existing categorisation patterns. This feature extracts keywords from conversations, stores them with sentiment analysis and confidence scores, and supports word cloud visualization aggregated per operation.

Key Decisions
Decision

Choice

Keyword Mode

Both Modes - predefined keywords + AI-discovered keywords

Kafka Topic

Reuse TOPIC_QUALIFICATION_REQUEST with action: 'keyword_extraction'

Word Cloud Scope

Per Operation aggregation

Data Models
1. KeywordGroup
Collection: keyword_groups (MongoDB)

Field

Type

Description

_id

ObjectId

Primary key

tenant_id

integer

Tenant isolation

operation_id

integer

Operation reference

name

string

Group name

description

string (nullable)

Group description

deleted_at

timestamp

Soft delete

created_at

timestamp

Creation time

updated_at

timestamp

Last update

2. Keyword
Collection: keywords (MongoDB)

Field

Type

Description

_id

ObjectId

Primary key

keyword_group_id

ObjectId

References keyword_groups

tenant_id

integer

Tenant isolation

operation_id

integer

Operation reference

value

string

The actual keyword/phrase

deleted_at

timestamp

Soft delete

created_at

timestamp

Creation time

updated_at

timestamp

Last update

3. KeywordResult
Collection: keyword_results (MongoDB)

One record per conversation + keyword pair.

Field

Type

Description

_id

ObjectId

Primary key

conv_id

ObjectId

References conversations

keyword_id

ObjectId (nullable)

References keywords (null for discovered)

value

string

The keyword text

sentiment

string

'positive', 'negative', 'neutral'

confidence_score

float

0-1 confidence value

occurrences

integer

Count in conversation

type

string

'auto' or 'manual'

 

 

 

deleted_at

timestamp

Soft delete

created_at

timestamp

Creation time

updated_at

timestamp

Last update

Note: Status is tracked on Conversation.status_keyword_extraction, not on individual KeywordResult records. KeywordResult records are created only after successful extraction.

Example:



{
  "_id": "ObjectId",
  "conv_id": "conversation_123",
  "keyword_id": null,
  "value": "customer satisfaction",
  "sentiment": "positive",
  "confidence_score": 0.92,
  "occurrences": 3,
  "type": "auto",
  "is_discovered": true
}
4. Conversation Model Updates
Add to Conversation model fillable:

want_keyword_extraction (boolean)

status_keyword_extraction (string)

lookup_keywords (array) - denormalized keyword results

Implementation Todo List
Phase 1: Models & Database
KeywordGroup Model (app/Models/keyword/KeywordGroup.php)

[ ] Extend MongoDB Model

[ ] Add soft deletes

[ ] Implement Multitenantable trait

[ ] Add scopeByUser() for access control

[ ] Add relationship to keywords()

[ ] Add relationship to operations() via GridOperation

Keyword Model (app/Models/keyword/Keyword.php)

[ ] Extend MongoDB Model

[ ] Add soft deletes

[ ] Implement Multitenantable trait

[ ] Add scopeByUser() scope

[ ] Add relationship belongsTo(KeywordGroup)

KeywordResult Model (app/Models/keyword/KeywordResult.php)

[ ] Extend MongoDB Model

[ ] Add soft deletes

[ ] Add boot hooks for updateConversationLookup() on create/update/delete

[ ] Add relationship belongsTo(Conversation) via conv_id

[ ] Add relationship belongsTo(Keyword) via keyword_id (nullable for discovered)

[ ] Add toConversationMetrics() method

Conversation Model Updates (app/Models/evaluation/Conversation.php)

[ ] Add want_keyword_extraction to fillable

[ ] Add status_keyword_extraction to fillable

[ ] Add lookup_keywords to fillable

[ ] Add keywordResults() relationship

[ ] Update boot method for cascade deletion

GridOperation Model

[ ] Ensure it supports grid_type: 'keyword'

Phase 2: Form Requests & Validation
KeywordGroupRequest (app/Http/Requests/KeywordGroupRequest.php)

[ ] Validate: name (required), description, operation_id, tenant_id

[ ] Validate: keywords array with value field

Phase 3: API Resources
[ ] KeywordGroupResource (app/Http/Resources/KeywordGroupResource.php)

Return: id, name, description, tenant_id, keywords, timestamps

[ ] KeywordResource (app/Http/Resources/KeywordResource.php)

Return: _id, value, keyword_group_id

[ ] KeywordResultResource (app/Http/Resources/KeywordResultResource.php)

Return: id, conv_id, keyword_id, value, sentiment, confidence_score, occurrences, type, is_discovered, created_at

Phase 4: Controllers
KeywordGroupController (app/Http/Controllers/keyword/KeywordGroupController.php)

[ ] index() - List groups with keywords (scoped by user)

[ ] store(KeywordGroupRequest) - Create group + link to operation

[ ] show(id) - Get single group with keywords

[ ] update(id) - Update group metadata

[ ] destroy(id) - Soft delete group and keywords

[ ] fullUpdate(id) - Full group + keywords update with transaction

[ ] getGroupsByOperation(operation_id) - Get active keyword groups for operation

[ ] trashed() - List soft-deleted groups

[ ] restore(array) - Restore trashed groups

[ ] forceDestroy(array) - Permanently delete

KeywordController (app/Http/Controllers/keyword/KeywordController.php)

[ ] destroy(id) - Delete single keyword

KeywordResultController (app/Http/Controllers/keyword/KeywordResultController.php)

[ ] findKeywords(conversation_id) - Get keyword results for conversation

[ ] manualKeyword(Request) - Manually add keyword to conversation

[ ] deleteKeyword(Request) - Remove keyword from conversation result

Phase 5: Routes
Create routes file (routes/evaluation/keyword.php)



// Keyword Group Management
GET    /v1/keyword-groups                     // List groups
POST   /v1/keyword-groups                     // Create group
GET    /v1/keyword-groups/{id}                // Show group
PUT    /v1/keyword-groups/{id}/update         // Full update
DELETE /v1/keyword-groups/{id}                // Delete group
// Keyword Management
DELETE /keywords/{id}                         // Delete keyword
// Soft Delete Operations
GET    /trash-keywords                        // List trashed
POST   /restore-keywords                      // Restore groups
POST   /force-delete-keywords                 // Permanently delete
// Operation-specific Groups
GET    /operations/{operation_id}/keyword-groups
// Conversation Keywords
GET    /conversations/{conversation_id}/keywords
POST   /manual-keyword
DELETE /delete-keyword
Register routes in routes/api.php

[ ] Add feature middleware: feature:keyword_extraction

[ ] Add auth/api_key_role middleware

Phase 6: Services
KafkaKeywordService (app/Services/Kafka/KafkaKeywordService.php)

launchKeywordExtraction(conv_id, model_ai):

[ ] Get active keyword groups for operation

[ ] Get predefined keywords to match against

[ ] Update conversation status_keyword_extraction: 'pending'

[ ] Build Kafka payload with transcript and predefined keywords

[ ] Publish to TOPIC_QUALIFICATION_REQUEST with action: 'keyword_extraction'

consumeKeywordResult(payload):

[ ] Validate payload structure

[ ] Handle status: FAILED, PENDING, DONE

[ ] Create one KeywordResult per extracted keyword:

Predefined matches: is_discovered: false, keyword_id: <id>

Discovered keywords: is_discovered: true, keyword_id: null

[ ] Trigger NotificationService

[ ] Update conversation status

Phase 7: Background Jobs
LaunchKeywordExtractionJob (app/Jobs/LaunchKeywordExtractionJob.php)

[ ] Dispatch keyword extraction to Kafka

[ ] Handle: conv_id, model_ai parameters

[ ] Call KafkaKeywordService::launchKeywordExtraction()

Phase 8: Feature Flag
[ ] Add feature flag for keyword_extraction

[ ] Add to features table/seeder

[ ] Enable toggle per tenant/team/user

Phase 9: Kafka Integration
[ ] Update Kafka consumer to handle keyword extraction responses

[ ] Route to KafkaKeywordService::consumeKeywordResult()

[ ] Handle action type 'keyword_extraction'

Phase 10: Testing
[ ] Create unit tests for models

[ ] Create feature tests for API endpoints

[ ] Test Kafka message flow

Phase 11: Word Cloud Aggregation (Future)
KeywordAggregationController

[ ] getWordCloud(operation_id) - Aggregate all keywords across operation's conversations

[ ] Return: keyword value, total occurrences, sentiment distribution, confidence avg

[ ] Support filtering by date range, conversation type

Aggregation Service

[ ] MongoDB aggregation pipeline for efficient keyword counting

[ ] Group by keyword value (both predefined and discovered)

[ ] Calculate frequency, sentiment breakdown

Frontend

[ ] Word cloud visualization (d3-cloud or similar library)

Reference Files (Existing Patterns)
Type

File Path

Model

app/Models/categorisation/CategorisationGrid.php

Model

app/Models/categorisation/CategorisationTag.php

Model

app/Models/categorisation/CategorisationResult.php

Controller

app/Http/Controllers/categorisation/CategorisationGridController.php

Controller

app/Http/Controllers/categorisation/CategorisationController.php

Service

app/Services/Kafka/KafkaCategorisationService.php

Job

app/Jobs/LaunchCategorisationJob.php

Routes

routes/evaluation/categorisation.php

Request

app/Http/Requests/CategorisationGridRequest.php

Notes
1. Naming Convention
Using keyword_groups instead of keyword_grids to align with original model names.

2. Sentiment Analysis
KeywordResult stores sentiment per keyword, enabling richer analysis than categorisation.

3. Both Modes - Predefined + Discovered Keywords
Predefined Keywords:

Keywords defined in KeywordGroup

Marked with is_discovered: false

Have valid keyword_id reference

Discovered Keywords:

AI-extracted new keywords

Marked with is_discovered: true

Have keyword_id: null

Both types contribute to word cloud aggregation.

4. GridOperation Integration
Keyword groups link to operations via GridOperation table with grid_type: 'keyword'.

5. Kafka Integration
Reuses TOPIC_QUALIFICATION_REQUEST topic with action: 'keyword_extraction'.