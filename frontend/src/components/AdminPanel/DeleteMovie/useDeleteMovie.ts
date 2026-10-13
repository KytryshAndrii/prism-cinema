import {  useState } from 'react';
import {
  useGetMoviesQuery,
  useDeleteMovieMutation,
  useSearchMoviesQuery,
} from '../../../api/authApi';
import type { tMovieResponse } from '../../../types/authTypes';

type tAlertState = {
  type: 'success' | 'error';
  message: string;
} | null;

export const useDeleteMovie = () => {
  const [searchPhrase, setSearchPhrase] = useState('');
  const [movieToDelete, setMovieToDelete] = useState<tMovieResponse | null>(null);
  const [alert, setAlert] = useState<tAlertState>(null);

  const {
    data: allMovies,
    isLoading: isLoadingAll,
  } = useGetMoviesQuery(undefined, { skip: !!searchPhrase });

  const {
    data: searchedMovies,
    isFetching: isFetchingSearch,
  } = useSearchMoviesQuery(searchPhrase, {
    skip: !searchPhrase,
  });

  const [deleteMovie, { isLoading: isDeleting }] = useDeleteMovieMutation();

  const handleSearchChange = (value: string) => {
    setSearchPhrase(value);
  };

  const confirmDelete = async () => {
    if (!movieToDelete || isDeleting) return;

    try {
      await deleteMovie(movieToDelete.movie_id).unwrap();
      setAlert({
        type: 'success',
        message: 'Movie deleted successfully',
      });
    } catch (err: any) {
      const status = err?.status;
      setAlert({
        type: 'error',
        message:
          status === 404
            ? 'Movie not found'
            : 'Server error. Please try again later.',
      });
    } finally {
      setMovieToDelete(null);
    }
  };

  const openDeleteModal = (movie: tMovieResponse) => {
    setMovieToDelete(movie);
  };

  const cancelDelete = () => {
    setMovieToDelete(null);
  };

  const closeAlert = () => {
    setAlert(null);
  };

  const displayedMovies = searchPhrase ? searchedMovies : allMovies;

  return {
    movies: displayedMovies ?? [],
    searchPhrase,
    handleSearchChange,
    openDeleteModal,
    confirmDelete,
    cancelDelete,
    movieToDelete,
    alert,
    closeAlert,
    isDeleting,
    isLoading: isLoadingAll || isFetchingSearch,
  };
};

