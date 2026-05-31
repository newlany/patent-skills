# CN Procedural Reference

This page is a source checklist for Chinese patent drafting workflows. It is not a substitute for a final filing review. Before filing or making procedural assertions, re-check the linked official source and record the access date in the filing checklist or `输出/定稿/验证报告.md`.

Last checked: 2026-04-25.

## Official Entry Points

- CNIPA patent application matters: https://www.cnipa.gov.cn/art/2020/6/5/art_1517_92472.html
- CNIPA Patent Examination Guidelines PDF: https://www.cnipa.gov.cn/module/download/downfile.jsp?classid=0&filename=5753f257e6a04b6f8e305eb6d34ba452.pdf&showname=%E4%B8%93%E5%88%A9%E5%AE%A1%E6%9F%A5%E6%8C%87%E5%8D%97.pdf
- CNIPA electronic XML filing notice, published 2025-11-12: https://www.cnipa.gov.cn/art/2025/11/12/art_75_202551.html
- Patent Business Handling System: http://cponline.cnipa.gov.cn

## Drafting Facts To Verify

Use the links above to verify these procedural facts before filing:

- For an invention application, CNIPA’s application-matters page lists the application documents as request, abstract, claims, specification, and drawings when necessary.
- For a utility model application, abstract drawing and specification drawings are normally part of the listed application documents.
- CNIPA’s application-matters page lists a filing-order discipline for invention and utility-model paper/application files: request, abstract, abstract drawing, claims, specification, and specification drawings.
- The Examination Guidelines describe the usual specification order: technical field, background art, invention content, drawings description when drawings exist, and embodiments.
- The Examination Guidelines continue to treat the abstract text as no more than 300 Chinese characters including punctuation, and abstract drawing/reference-sign handling should be checked.
- From 2026-01-01, CNIPA’s XML notice states that electronic patent application, reexamination, invalidity, and related procedural documents submitted electronically should be submitted in XML format, and non-XML electronic patent files are no longer accepted.
- CNIPA’s XML notice points users to the Patent Business Handling System tools/download area for XML standards, conversion tools, and user manuals.

## Workflow Use

During drafting:

- treat this page as a live-source pointer, not frozen legal advice
- do not infer fee, deadline, applicant identity, inventor identity, priority, or secrecy-review facts from drafting documents alone
- record any procedural assumption in the relevant stage memo
- run `scripts/patent_qc_micro.py check` for deterministic first-pass checks, then use the dedicated QC skills for legal and technical judgment

Before final package:

- verify the current filing-channel requirements from CNIPA or the Patent Business Handling System
- confirm whether the output package must be XML, DOCX, PDF, or another office-specific format for the actual filing path
- keep the editable source and converted/submitted package together under `输出/定稿/`
- register source links, access date, and final artifacts in `manifest.json`
