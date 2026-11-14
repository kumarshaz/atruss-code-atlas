---
title: Architecture — hs-web/hsweb-framework
description: Arc42 and Pipeline report for hs-web/hsweb-framework
---

# Repository Architecture Analysis: hs-web/hsweb-framework

## Metadata
- **SHA**: `f2617a56d8b1d5b11e2bb504b8d419406eba7116`
- **Primary Ecosystem**: Java

## Quality Metrics
- **avg_cyclomatic_complexity**: 3.15
- **component_count**: 68
- **files_analyzed**: 2218
- **framework**: Spring Boot
- **loc**: 201881
- **max_cyclomatic_complexity**: 155
- **sloc**: 144222

# Architecture: hs-web/hsweb-framework

## Context
- **Repository**: `hs-web/hsweb-framework`
- **SHA**: `f2617a56d8b1d5b11e2bb504b8d419406eba7116`
- **Ecosystem**: Java
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    repo_root(["hs-web/hsweb-framework (68 components)"])
    dir_0_hsweb_system["hsweb-system (25)"]
    repo_root --> dir_0_hsweb_system
    sub_0_0_hsweb_system_authorization["hsweb-system-authorization (15)"]
    dir_0_hsweb_system --> sub_0_0_hsweb_system_authorization
    sub_0_1_hsweb_system_dictionary["hsweb-system-dictionary (5)"]
    dir_0_hsweb_system --> sub_0_1_hsweb_system_dictionary
    sub_0_2_hsweb_system_file["hsweb-system-file (4)"]
    dir_0_hsweb_system --> sub_0_2_hsweb_system_file
    sub_0_more["+1 more submodules (1)"]
    dir_0_hsweb_system --> sub_0_more
    dir_1_hsweb_authorization["hsweb-authorization (14)"]
    repo_root --> dir_1_hsweb_authorization
    sub_1_0_hsweb_authorization_basic["hsweb-authorization-basic (9)"]
    dir_1_hsweb_authorization --> sub_1_0_hsweb_authorization_basic
    sub_1_1_hsweb_authorization_oauth2["hsweb-authorization-oauth2 (3)"]
    dir_1_hsweb_authorization --> sub_1_1_hsweb_authorization_oauth2
    sub_1_2__module_root_["(module root) (1)"]
    dir_1_hsweb_authorization --> sub_1_2__module_root_
    sub_1_more["+1 more submodules (1)"]
    dir_1_hsweb_authorization --> sub_1_more
    dir_2_hsweb_commons["hsweb-commons (13)"]
    repo_root --> dir_2_hsweb_commons
    sub_2_0_hsweb_commons_crud["hsweb-commons-crud (11)"]
    dir_2_hsweb_commons --> sub_2_0_hsweb_commons_crud
    sub_2_1__module_root_["(module root) (1)"]
    dir_2_hsweb_commons --> sub_2_1__module_root_
    sub_2_2_hsweb_commons_api["hsweb-commons-api (1)"]
    dir_2_hsweb_commons --> sub_2_2_hsweb_commons_api
    dir_3_hsweb_concurrent["hsweb-concurrent (4)"]
    repo_root --> dir_3_hsweb_concurrent
    dir_4_hsweb_logging["hsweb-logging (4)"]
    repo_root --> dir_4_hsweb_logging
    dir_other_modules["+4 more modules (8)"]
    repo_root --> dir_other_modules
```

## Component Details

Showing top 60 representative components out of 68 across 9 module group(s):

- **Module `hsweb-system`** (25 components — API_ROUTE: 10, CONFIG: 8, MODULE: 7)
- **Module `hsweb-authorization`** (14 components — CONFIG: 5, API_ROUTE: 5, MODULE: 4)
- **Module `hsweb-commons`** (13 components — API_ROUTE: 4, MODULE: 3, CONFIG: 3)
- **Module `hsweb-concurrent`** (4 components — MODULE: 2, CONFIG: 2)
- **Module `hsweb-logging`** (4 components — MODULE: 3, CONFIG: 1)
- **Module `hsweb-datasource`** (3 components — MODULE: 2, CONFIG: 1)
- **Module `hsweb-starter`** (3 components — CONFIG: 2, MODULE: 1)
- **Module `(root)`** (1 components — MODULE: 1)
- **Module `hsweb-core`** (1 components — MODULE: 1)

- **OAuth2AuthorizeController** (`hsweb-authorization/hsweb-authorization-oauth2/src/main/java/org/hswebframework/web/oauth2/server/web/OAuth2AuthorizeController.java`): API_ROUTE (deps: OAuth2Properties)
- **ReactiveFileController** (`hsweb-system/hsweb-system-file/src/main/java/org/hswebframework/web/file/web/ReactiveFileController.java`): API_ROUTE (deps: FileUploadProperties)
- **WebFluxAuthorizationSettingController** (`hsweb-system/hsweb-system-authorization/hsweb-system-authorization-default/src/main/java/org/hswebframework/web/system/authorization/defaults/webflux/WebFluxAuthorizationSettingController.java`): API_ROUTE (deps: PermissionProperties)
- **WebFluxPermissionController** (`hsweb-system/hsweb-system-authorization/hsweb-system-authorization-default/src/main/java/org/hswebframework/web/system/authorization/defaults/webflux/WebFluxPermissionController.java`): API_ROUTE (deps: PermissionProperties)
- **AopAccessLoggerSupportAutoConfiguration** (`hsweb-logging/hsweb-access-logging-aop/src/main/java/org/hswebframework/web/logging/aop/AopAccessLoggerSupportAutoConfiguration.java`): CONFIG
- **AopAuthorizeAutoConfiguration** (`hsweb-authorization/hsweb-authorization-basic/src/main/java/org/hswebframework/web/authorization/basic/configuration/AopAuthorizeAutoConfiguration.java`): CONFIG
- **AopDataSourceSwitcherAutoConfiguration** (`hsweb-datasource/hsweb-datasource-api/src/main/java/org/hswebframework/web/datasource/AopDataSourceSwitcherAutoConfiguration.java`): CONFIG
- **AuthenticationInitializeProperties** (`hsweb-system/hsweb-system-authorization/hsweb-system-authorization-default/src/main/java/org/hswebframework/web/system/authorization/defaults/service/AuthenticationInitializeProperties.java`): CONFIG
- **AuthorizationController** (`hsweb-authorization/hsweb-authorization-basic/src/main/java/org/hswebframework/web/authorization/basic/web/AuthorizationController.java`): API_ROUTE
- **CommonErrorControllerAdvice** (`hsweb-commons/hsweb-commons-crud/src/main/java/org/hswebframework/web/crud/web/CommonErrorControllerAdvice.java`): API_ROUTE
- **CommonWebMvcErrorControllerAdvice** (`hsweb-commons/hsweb-commons-crud/src/main/java/org/hswebframework/web/crud/web/CommonWebMvcErrorControllerAdvice.java`): API_ROUTE
- **CorsProperties** (`hsweb-starter/src/main/java/org/hswebframework/web/starter/CorsProperties.java`): CONFIG
- **DictionaryProperties** (`hsweb-system/hsweb-system-dictionary/src/main/java/org/hswebframework/web/dictionary/configuration/DictionaryProperties.java`): CONFIG
- **EasyormProperties** (`hsweb-commons/hsweb-commons-crud/src/main/java/org/hswebframework/web/crud/configuration/EasyormProperties.java`): CONFIG
- **EmbedAuthenticationProperties** (`hsweb-authorization/hsweb-authorization-basic/src/main/java/org/hswebframework/web/authorization/basic/embed/EmbedAuthenticationProperties.java`): CONFIG
- **FileUploadProperties** (`hsweb-system/hsweb-system-file/src/main/java/org/hswebframework/web/file/FileUploadProperties.java`): CONFIG
- **FluxTestController** (`hsweb-authorization/hsweb-authorization-basic/src/test/java/org/hswebframework/web/authorization/basic/aop/FluxTestController.java`): API_ROUTE
- **OAuth2Properties** (`hsweb-authorization/hsweb-authorization-oauth2/src/main/java/org/hswebframework/web/oauth2/server/OAuth2Properties.java`): CONFIG
- **PagerQueryProperties** (`hsweb-commons/hsweb-commons-crud/src/main/java/org/hswebframework/web/crud/web/PagerQueryProperties.java`): CONFIG
- **PermissionProperties** (`hsweb-system/hsweb-system-authorization/hsweb-system-authorization-default/src/main/java/org/hswebframework/web/system/authorization/defaults/configuration/PermissionProperties.java`): CONFIG
- **R2dbcErrorControllerAdvice** (`hsweb-commons/hsweb-commons-crud/src/main/java/org/hswebframework/web/crud/web/R2dbcErrorControllerAdvice.java`): API_ROUTE
- **ReactiveCacheProperties** (`hsweb-concurrent/hsweb-concurrent-cache/src/main/java/org/hswebframework/web/cache/configuration/ReactiveCacheProperties.java`): CONFIG
- **ReactiveTestApplication** (`hsweb-system/hsweb-system-authorization/hsweb-system-authorization-default/src/test/java/org/hswebframework/web/system/authorization/defaults/service/reactive/ReactiveTestApplication.java`): CONFIG
- **ReactiveTestApplication** (`hsweb-system/hsweb-system-authorization/hsweb-system-authorization-oauth2/src/test/java/org/hswebframework/web/oauth2/ReactiveTestApplication.java`): CONFIG
- **ReactiveTestApplication** (`hsweb-system/hsweb-system-dictionary/src/test/java/org/hswebframework/web/dictionary/ReactiveTestApplication.java`): CONFIG
- **ReactiveUserTokenController** (`hsweb-authorization/hsweb-authorization-basic/src/main/java/org/hswebframework/web/authorization/basic/web/ReactiveUserTokenController.java`): API_ROUTE
- **ResponseMessageWrapperAdvice** (`hsweb-commons/hsweb-commons-crud/src/main/java/org/hswebframework/web/crud/web/ResponseMessageWrapperAdvice.java`): API_ROUTE
- **TestApplication** (`hsweb-authorization/hsweb-authorization-basic/src/test/java/org/hswebframework/web/authorization/basic/aop/TestApplication.java`): CONFIG
- **TestApplication** (`hsweb-commons/hsweb-commons-crud/src/test/java/org/hswebframework/web/crud/TestApplication.java`): CONFIG
- **TestApplication** (`hsweb-concurrent/hsweb-concurrent-cache/src/test/java/org/hswebframework/web/cache/TestApplication.java`): CONFIG
- **TestApplication** (`hsweb-starter/src/test/java/org/hswebframework/web/starter/initialize/TestApplication.java`): CONFIG
- **TestApplication** (`hsweb-system/hsweb-system-file/src/test/java/org/hswebframework/web/file/web/TestApplication.java`): CONFIG
- **TestCacheEntityService** (`hsweb-commons/hsweb-commons-crud/src/test/java/org/hswebframework/web/crud/service/TestCacheEntityService.java`): SERVICE
- **TestController** (`hsweb-authorization/hsweb-authorization-basic/src/test/java/org/hswebframework/web/authorization/basic/aop/TestController.java`): API_ROUTE
- **TestEntityService** (`hsweb-commons/hsweb-commons-crud/src/test/java/org/hswebframework/web/crud/service/TestEntityService.java`): SERVICE
- **TestTreeSortEntityService** (`hsweb-commons/hsweb-commons-crud/src/test/java/org/hswebframework/web/crud/service/TestTreeSortEntityService.java`): SERVICE
- **UserAllowPermissionHandler** (`hsweb-authorization/hsweb-authorization-basic/src/main/java/org/hswebframework/web/authorization/basic/handler/UserAllowPermissionHandler.java`): CONFIG
- **WebFluxDimensionController** (`hsweb-system/hsweb-system-authorization/hsweb-system-authorization-default/src/main/java/org/hswebframework/web/system/authorization/defaults/webflux/WebFluxDimensionController.java`): API_ROUTE
- **WebFluxDimensionTypeController** (`hsweb-system/hsweb-system-authorization/hsweb-system-authorization-default/src/main/java/org/hswebframework/web/system/authorization/defaults/webflux/WebFluxDimensionTypeController.java`): API_ROUTE
- **WebFluxDimensionUserController** (`hsweb-system/hsweb-system-authorization/hsweb-system-authorization-default/src/main/java/org/hswebframework/web/system/authorization/defaults/webflux/WebFluxDimensionUserController.java`): API_ROUTE
- **WebFluxOAuth2ClientController** (`hsweb-system/hsweb-system-authorization/hsweb-system-authorization-oauth2/src/main/java/org/hswebframework/web/oauth2/web/WebFluxOAuth2ClientController.java`): API_ROUTE
- **WebFluxUserController** (`hsweb-system/hsweb-system-authorization/hsweb-system-authorization-default/src/main/java/org/hswebframework/web/system/authorization/defaults/webflux/WebFluxUserController.java`): API_ROUTE
- **WebfluxDictionaryController** (`hsweb-system/hsweb-system-dictionary/src/main/java/org/hswebframework/web/dictionary/webflux/WebfluxDictionaryController.java`): API_ROUTE
- **WebfluxDictionaryItemController** (`hsweb-system/hsweb-system-dictionary/src/main/java/org/hswebframework/web/dictionary/webflux/WebfluxDictionaryItemController.java`): API_ROUTE
- **hsweb-access-logging-aop** (`hsweb-logging/hsweb-access-logging-aop/pom.xml`): MODULE
- **hsweb-access-logging-api** (`hsweb-logging/hsweb-access-logging-api/pom.xml`): MODULE
- **hsweb-authorization** (`hsweb-authorization/pom.xml`): MODULE
- **hsweb-authorization-api** (`hsweb-authorization/hsweb-authorization-api/pom.xml`): MODULE
- **hsweb-authorization-basic** (`hsweb-authorization/hsweb-authorization-basic/pom.xml`): MODULE
- **hsweb-authorization-oauth2** (`hsweb-authorization/hsweb-authorization-oauth2/pom.xml`): MODULE
- **hsweb-commons** (`hsweb-commons/pom.xml`): MODULE
- **hsweb-commons-api** (`hsweb-commons/hsweb-commons-api/pom.xml`): MODULE
- **hsweb-commons-crud** (`hsweb-commons/hsweb-commons-crud/pom.xml`): MODULE
- **hsweb-concurrent** (`hsweb-concurrent/pom.xml`): MODULE
- **hsweb-concurrent-cache** (`hsweb-concurrent/hsweb-concurrent-cache/pom.xml`): MODULE
- **hsweb-core** (`hsweb-core/pom.xml`): MODULE
- **hsweb-datasource** (`hsweb-datasource/pom.xml`): MODULE
- **hsweb-datasource-api** (`hsweb-datasource/hsweb-datasource-api/pom.xml`): MODULE
- **hsweb-framework** (`pom.xml`): MODULE
- **hsweb-logging** (`hsweb-logging/pom.xml`): MODULE


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
