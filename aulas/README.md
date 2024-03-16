# CONTROLE DE AULAS

- [x] #A2379
- [x] #A2380
- [x] #A2381
- [x] #A2382
- [x] #A2383
- [x] #A2384
- [x] #A2385
- [x] #A2386
- [x] #A2387
- [x] #A2388
- [x] #A2389
- [x] #A2390
- [x] #A2391
- [x] #A2392
- [x] #A2393
- [x] #A2394
- [x] #A2395
- [x] #A2396
- [x] #A2397
- [x] #A2398
- [x] #A2399
- [x] #A2400
- [x] #A2401
- [x] #A2402
- [x] #A2403
- [x] #A2404
- [x] #A2405
- [x] #A2406
- [x] #A2407
- [x] #A2408
- [x] #A2409
- [ ] #A2410
- [ ] #A2411
- [ ] #A2412
- [ ] #A2413
- [ ] #A2414
- [ ] #A2415
- [ ] #A2416
- [ ] #A2417
- [ ] #A2418
- [ ] #A2419
- [ ] #A2420
- [ ] #A2421
- [ ] #A2422
- [ ] #A2423
- [ ] #A2424
- [ ] #A2425
- [ ] #A2426
- [ ] #A2427
- [ ] #A2428
- [ ] #A2429
- [ ] #A2430
- [ ] #A2431
- [ ] #A2432
- [ ] #A2433
- [ ] #A2434
- [ ] #A2435
- [ ] #A2436
- [ ] #A2437
- [ ] #A2438
- [ ] #A2439
- [ ] #A2440
- [ ] #A2441


# Anotações:

## Pesquisar
- Verificar a diferença de MagickMock para create_autospec
- List  comprehension


## TDD
- Trate as exeções de acordo com seu domínio. Não faça um teste que interaga diramente com diferentes camadas.

## Inversão de Dependência:
- Módulos de maior nível não podem depender de módulos de menor nível. Deve-se criar interfaces que façam tanto o módulo de maior nível quanto de menor dependerem dele.

## DTO:
- Sempre que puder utilizar dto de entrada e de saída.

## Regras Category
- [x] Nome da categoria deverá ser obrigatório.
- [x] Nome deverá ter no máximo 255 caracteres.
- [x] Ao criar uma nova categoria um identificador deve ser gerado no formato (uuid).
- [x] Ao criar uma categoria os campos id, descrição e isActive não serão obrigatórios.
- [x] Caso a propiedade isActive não seja informada, deverá receber como default o valor true.
- [x] Test __str__
- [x] Tes __repr__
- [x] Deve permitir a alteração da categoria informando o nome e a descrição
- [X] Deve permitir ativar e desativar uma categoria

