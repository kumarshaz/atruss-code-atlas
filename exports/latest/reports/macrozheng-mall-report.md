---
title: Architecture — macrozheng/mall
description: Arc42 and Pipeline report for macrozheng/mall
---

# Repository Architecture Analysis: macrozheng/mall

## Metadata
- **SHA**: `dcaa93b3150352e5044708d7211b5bed0af4509f`
- **Primary Ecosystem**: Java

## Quality Metrics
- **avg_cyclomatic_complexity**: 2.86
- **component_count**: 132
- **files_analyzed**: 1048
- **framework**: Spring Boot
- **loc**: 170868
- **max_cyclomatic_complexity**: 74
- **sloc**: 131174

# Architecture: macrozheng/mall

## Context
- **Repository**: `macrozheng/mall`
- **SHA**: `dcaa93b3150352e5044708d7211b5bed0af4509f`
- **Ecosystem**: Java
- **Framework**: Unknown

## Building Block View

```mermaid
graph TD;
    repo_root(["macrozheng/mall (132 components)"])
    dir_0_mall_admin["mall-admin (69)"]
    repo_root --> dir_0_mall_admin
    sub_0_0_src["src (68)"]
    dir_0_mall_admin --> sub_0_0_src
    sub_0_1__module_root_["(module root) (1)"]
    dir_0_mall_admin --> sub_0_1__module_root_
    dir_1_mall_portal["mall-portal (39)"]
    repo_root --> dir_1_mall_portal
    sub_1_0_src["src (38)"]
    dir_1_mall_portal --> sub_1_0_src
    sub_1_1__module_root_["(module root) (1)"]
    dir_1_mall_portal --> sub_1_1__module_root_
    dir_2_mall_demo["mall-demo (9)"]
    repo_root --> dir_2_mall_demo
    sub_2_0_src["src (8)"]
    dir_2_mall_demo --> sub_2_0_src
    sub_2_1__module_root_["(module root) (1)"]
    dir_2_mall_demo --> sub_2_1__module_root_
    dir_3_mall_search["mall-search (6)"]
    repo_root --> dir_3_mall_search
    dir_4_mall_security["mall-security (5)"]
    repo_root --> dir_4_mall_security
    dir_other_modules["+3 more modules (4)"]
    repo_root --> dir_other_modules
    sub_0_0_src -.->|"1 dep"| sub_2_0_src
    sub_2_0_src -.->|"1 dep"| dir_4_mall_security
```

## Component Details

Showing top 60 representative components out of 132 across 8 module group(s):

- **Module `mall-admin`** (69 components — API_ROUTE: 31, SERVICE: 31, CONFIG: 6)
- **Module `mall-portal`** (39 components — SERVICE: 15, API_ROUTE: 13, CONFIG: 10)
- **Module `mall-demo`** (9 components — CONFIG: 5, API_ROUTE: 2, MODULE: 1)
- **Module `mall-search`** (6 components — CONFIG: 3, MODULE: 1, API_ROUTE: 1)
- **Module `mall-security`** (5 components — CONFIG: 4, MODULE: 1)
- **Module `mall-common`** (2 components — MODULE: 1, API_ROUTE: 1)
- **Module `(root)`** (1 components — MODULE: 1)
- **Module `mall-mbg`** (1 components — MODULE: 1)

- **AlipayClientConfig** (`mall-portal/src/main/java/com/macro/mall/portal/config/AlipayClientConfig.java`): CONFIG (deps: AlipayConfig)
- **AlipayController** (`mall-portal/src/main/java/com/macro/mall/portal/controller/AlipayController.java`): API_ROUTE (deps: AlipayConfig)
- **AlipayServiceImpl** (`mall-portal/src/main/java/com/macro/mall/portal/service/impl/AlipayServiceImpl.java`): SERVICE (deps: AlipayConfig)
- **CommonSecurityConfig** (`mall-security/src/main/java/com/macro/mall/security/config/CommonSecurityConfig.java`): CONFIG (deps: IgnoreUrlsConfig)
- **MallSecurityConfig** (`mall-admin/src/main/java/com/macro/mall/config/MallSecurityConfig.java`): CONFIG (deps: SecurityConfig)
- **SecurityConfig** (`mall-security/src/main/java/com/macro/mall/security/config/SecurityConfig.java`): CONFIG (deps: IgnoreUrlsConfig)
- **AlipayConfig** (`mall-portal/src/main/java/com/macro/mall/portal/config/AlipayConfig.java`): CONFIG
- **CmsPrefrenceAreaController** (`mall-admin/src/main/java/com/macro/mall/controller/CmsPrefrenceAreaController.java`): API_ROUTE
- **CmsPrefrenceAreaServiceImpl** (`mall-admin/src/main/java/com/macro/mall/service/impl/CmsPrefrenceAreaServiceImpl.java`): SERVICE
- **CmsSubjectController** (`mall-admin/src/main/java/com/macro/mall/controller/CmsSubjectController.java`): API_ROUTE
- **CmsSubjectServiceImpl** (`mall-admin/src/main/java/com/macro/mall/service/impl/CmsSubjectServiceImpl.java`): SERVICE
- **DemoController** (`mall-demo/src/main/java/com/macro/mall/demo/controller/DemoController.java`): API_ROUTE
- **DemoServiceImpl** (`mall-demo/src/main/java/com/macro/mall/demo/service/impl/DemoServiceImpl.java`): SERVICE
- **EsProductController** (`mall-search/src/main/java/com/macro/mall/search/controller/EsProductController.java`): API_ROUTE
- **EsProductServiceImpl** (`mall-search/src/main/java/com/macro/mall/search/service/impl/EsProductServiceImpl.java`): SERVICE
- **GlobalCorsConfig** (`mall-admin/src/main/java/com/macro/mall/config/GlobalCorsConfig.java`): CONFIG
- **GlobalCorsConfig** (`mall-portal/src/main/java/com/macro/mall/portal/config/GlobalCorsConfig.java`): CONFIG
- **GlobalExceptionHandler** (`mall-common/src/main/java/com/macro/mall/common/exception/GlobalExceptionHandler.java`): API_ROUTE
- **HomeController** (`mall-portal/src/main/java/com/macro/mall/portal/controller/HomeController.java`): API_ROUTE
- **HomeServiceImpl** (`mall-portal/src/main/java/com/macro/mall/portal/service/impl/HomeServiceImpl.java`): SERVICE
- **IgnoreUrlsConfig** (`mall-security/src/main/java/com/macro/mall/security/config/IgnoreUrlsConfig.java`): CONFIG
- **JacksonConfig** (`mall-portal/src/main/java/com/macro/mall/portal/config/JacksonConfig.java`): CONFIG
- **MallAdminApplication** (`mall-admin/src/main/java/com/macro/mall/MallAdminApplication.java`): CONFIG
- **MallDemoApplication** (`mall-demo/src/main/java/com/macro/mall/demo/MallDemoApplication.java`): CONFIG
- **MallPortalApplication** (`mall-portal/src/main/java/com/macro/mall/portal/MallPortalApplication.java`): CONFIG
- **MallSearchApplication** (`mall-search/src/main/java/com/macro/mall/search/MallSearchApplication.java`): CONFIG
- **MallSecurityConfig** (`mall-portal/src/main/java/com/macro/mall/portal/config/MallSecurityConfig.java`): CONFIG
- **MemberAttentionController** (`mall-portal/src/main/java/com/macro/mall/portal/controller/MemberAttentionController.java`): API_ROUTE
- **MemberAttentionServiceImpl** (`mall-portal/src/main/java/com/macro/mall/portal/service/impl/MemberAttentionServiceImpl.java`): SERVICE
- **MemberCollectionServiceImpl** (`mall-portal/src/main/java/com/macro/mall/portal/service/impl/MemberCollectionServiceImpl.java`): SERVICE
- **MemberProductCollectionController** (`mall-portal/src/main/java/com/macro/mall/portal/controller/MemberProductCollectionController.java`): API_ROUTE
- **MemberReadHistoryController** (`mall-portal/src/main/java/com/macro/mall/portal/controller/MemberReadHistoryController.java`): API_ROUTE
- **MemberReadHistoryServiceImpl** (`mall-portal/src/main/java/com/macro/mall/portal/service/impl/MemberReadHistoryServiceImpl.java`): SERVICE
- **MinioController** (`mall-admin/src/main/java/com/macro/mall/controller/MinioController.java`): API_ROUTE
- **MyBatisConfig** (`mall-admin/src/main/java/com/macro/mall/config/MyBatisConfig.java`): CONFIG
- **MyBatisConfig** (`mall-demo/src/main/java/com/macro/mall/demo/config/MyBatisConfig.java`): CONFIG
- **MyBatisConfig** (`mall-portal/src/main/java/com/macro/mall/portal/config/MyBatisConfig.java`): CONFIG
- **MyBatisConfig** (`mall-search/src/main/java/com/macro/mall/search/config/MyBatisConfig.java`): CONFIG
- **OmsCartItemController** (`mall-portal/src/main/java/com/macro/mall/portal/controller/OmsCartItemController.java`): API_ROUTE
- **OmsCartItemServiceImpl** (`mall-portal/src/main/java/com/macro/mall/portal/service/impl/OmsCartItemServiceImpl.java`): SERVICE
- **OmsCompanyAddressController** (`mall-admin/src/main/java/com/macro/mall/controller/OmsCompanyAddressController.java`): API_ROUTE
- **OmsCompanyAddressServiceImpl** (`mall-admin/src/main/java/com/macro/mall/service/impl/OmsCompanyAddressServiceImpl.java`): SERVICE
- **OmsOrderController** (`mall-admin/src/main/java/com/macro/mall/controller/OmsOrderController.java`): API_ROUTE
- **OmsOrderReturnApplyController** (`mall-admin/src/main/java/com/macro/mall/controller/OmsOrderReturnApplyController.java`): API_ROUTE
- **OmsOrderReturnApplyServiceImpl** (`mall-admin/src/main/java/com/macro/mall/service/impl/OmsOrderReturnApplyServiceImpl.java`): SERVICE
- **OmsOrderReturnReasonController** (`mall-admin/src/main/java/com/macro/mall/controller/OmsOrderReturnReasonController.java`): API_ROUTE
- **OmsOrderReturnReasonServiceImpl** (`mall-admin/src/main/java/com/macro/mall/service/impl/OmsOrderReturnReasonServiceImpl.java`): SERVICE
- **OmsOrderServiceImpl** (`mall-admin/src/main/java/com/macro/mall/service/impl/OmsOrderServiceImpl.java`): SERVICE
- **OmsOrderSettingController** (`mall-admin/src/main/java/com/macro/mall/controller/OmsOrderSettingController.java`): API_ROUTE
- **OmsOrderSettingServiceImpl** (`mall-admin/src/main/java/com/macro/mall/service/impl/OmsOrderSettingServiceImpl.java`): SERVICE
- **OmsPortalOrderController** (`mall-portal/src/main/java/com/macro/mall/portal/controller/OmsPortalOrderController.java`): API_ROUTE
- **OmsPortalOrderReturnApplyController** (`mall-portal/src/main/java/com/macro/mall/portal/controller/OmsPortalOrderReturnApplyController.java`): API_ROUTE
- **OmsPortalOrderReturnApplyServiceImpl** (`mall-portal/src/main/java/com/macro/mall/portal/service/impl/OmsPortalOrderReturnApplyServiceImpl.java`): SERVICE
- **OmsPortalOrderServiceImpl** (`mall-portal/src/main/java/com/macro/mall/portal/service/impl/OmsPortalOrderServiceImpl.java`): SERVICE
- **OmsPromotionServiceImpl** (`mall-portal/src/main/java/com/macro/mall/portal/service/impl/OmsPromotionServiceImpl.java`): SERVICE
- **OssConfig** (`mall-admin/src/main/java/com/macro/mall/config/OssConfig.java`): CONFIG
- **OssController** (`mall-admin/src/main/java/com/macro/mall/controller/OssController.java`): API_ROUTE
- **OssServiceImpl** (`mall-admin/src/main/java/com/macro/mall/service/impl/OssServiceImpl.java`): SERVICE
- **PmsBrandController** (`mall-admin/src/main/java/com/macro/mall/controller/PmsBrandController.java`): API_ROUTE
- **PmsBrandServiceImpl** (`mall-admin/src/main/java/com/macro/mall/service/impl/PmsBrandServiceImpl.java`): SERVICE


## CI/CD Pipeline Topology

```mermaid
graph TD;
  NoWorkflows[No Workflows Detected]
```
