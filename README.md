# codeflix-catalog-admin
Administração de Catálogo - Codeflix - Python

## Regras Category
- [x] Nome da categoria deverá ser obrigatório.
- [x] Nome deverá ter no máximo 255 caracteres.
- [x] Ao criar uma nova categoria um identificador deve ser gerado no formato (uuid).
- [x] Ao criar uma categoria os campos id, descrição e isActive não serão obrigatórios.
- [x] Caso a propiedade isActive não seja informada, deverá receber como default o valor true.
- [x] Test __str__
- [x] Tes __repr__
- [x] Deve permitir a alteração da categoria informando o nome e a descrição
- [ ] Deve permitir ativar e desativar uma categoria


## TDD
- Trate as exeções de acordo com seu domínio. Não faça um teste que interaga diramente com diferentes camadas.

## Inversão de Dependência:
- Módulos de maior nível não podem depender de módulos de menor nível. Deve-se criar interfaces que façam tanto o módulo de maior nível quanto de menor dependerem dele.
