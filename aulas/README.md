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
- [x] #A2410
- [x] #A2411
- [x] #A2412
- [x] #A2413
- [x] #A2414
- [x] #A2415
- [x] #A2416
- [x] #A2417
- [x] #A2418
- [x] #A2419
- [x] #A2420
- [x] #A2421
- [x] #A2422
- [x] #A2423
- [x] #A2424
- [x] #A2425
- [x] #A2426
- [x] #A2427
- [x] #A2428
- [x] #A2429
- [x] #A2430
- [x] #A2431
- [x] #A2432
- [x] #A2433
- [x] #A2434
- [ ] #A2435
- [ ] #A2436
- [ ] #A2437
- [ ] #A2438
- [ ] #A2439
- [ ] #A2440
- [ ] #A2441


# Anotações:

## Pesquisar
- Verificar a diferença de MagickMock para create_autospec:
    - MagicMock:
        - MagicMock é uma classe que cria objetos que respondem a qualquer chamada ou atribuição de atributo, retornando sempre um novo MagicMock. Isso significa que você pode chamar métodos e atributos inexistentes sem causar exceções.
        É útil quando você precisa de um objeto simulado que pode ser usado de forma flexível em muitos contextos diferentes.

    - create_autospec:
        - create_autospec é uma função que cria um objeto simulado com base em um objeto real, mas apenas copia a assinatura (métodos e atributos) do objeto real, substituindo as implementações por MagicMock por padrão.
        Ao contrário do MagicMock, create_autospec verifica se o objeto simulado se comporta exatamente como o objeto real. Isso significa que ele levantará uma exceção se você tentar chamar métodos ou atributos inexistentes no objeto real.
- List comprehension:
    - List comprehension é uma forma concisa e elegante de criar listas em Python. Ele permite que você crie uma lista derivada de outra lista existente aplicando uma expressão a cada item dessa lista. A estrutura básica de uma list comprehension é:
    ``` 
    numeros = [1, 2, 3, 4, 5]
    quadrados = [x**2 for x in numeros]
    print(quadrados)  # Saída: [1, 4, 9, 16, 25]
    ```

- pytest.mark.django_db


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


## Metas:
- Fazer um tutorial da documentação do Django por dia.
### Primeiros passos
- [ ] Parte 1: Requisições e respostas
- [ ] Parte 2: Modelos e o site Admin 
- [ ] Parte 3: Views e templates 
- [ ] Parte 4: Forms e views genéricas
- [ ] Parte 5: Testes 
- [ ] Parte 6: Arquivos estáticos 
- [ ] Parte 7: Personalizando o site admin 
- [ ] Como escrever aplicações reutilizáveis | Escrevendo seu primeiro patch para o Django

