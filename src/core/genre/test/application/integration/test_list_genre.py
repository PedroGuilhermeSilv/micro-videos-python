from src.core.genre.application.use_cases.list_genre import GenreResponse, ListGenre, ListGenreResponse
from src.core.genre.domain.genre import Genre
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository
from src.core.genre.infra.in_memory_genre import InMemoryGenreRepository
from src.core.category.domain.category import Category


class TestListGenre:
    def test_list_genres_with_categories(self):
        repository_category = InMemoryCategoryRepository()
        repository_genre = InMemoryGenreRepository()

        movie_category = Category(name="Movie")
        repository_category.save(movie_category)

        documentary_category = Category(name="Documentary")
        repository_category.save(documentary_category)
        
        genre = Genre(
            name="Action",
            categories={movie_category.id, documentary_category.id},
        )
        repository_genre.save(genre)

        use_case = ListGenre(repository=repository_genre)
        response = use_case.execute()

        assert response == ListGenreResponse(
            data=[
                GenreResponse(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=genre.categories,
                )
            ]
        )

    def test_list_genres_with_not_categories(self):
        repository_genre = InMemoryGenreRepository()
        
        genre = Genre(
            name="Action"
        )
        repository_genre.save(genre)

        use_case = ListGenre(repository=repository_genre)
        response = use_case.execute()

        assert response == ListGenreResponse(
            data=[
                GenreResponse(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=genre.categories,
                )
            ]
        )

