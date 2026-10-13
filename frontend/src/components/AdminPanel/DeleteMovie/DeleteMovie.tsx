import React from 'react';
import { Typography, IconButton, Modal, Button, Alert } from '@mui/material';
import {
  SearchBar,
  MovieItem,
  MovieList,
  TrashBin,
  ModalBox,
} from './styles';
import { FormWrapper } from '../styles';
import { useDeleteMovie } from './useDeleteMovie';

export const DeleteMovie: React.FC = () => {
  const {
    movies,
    searchPhrase,
    handleSearchChange,
    openDeleteModal,
    confirmDelete,
    cancelDelete,
    movieToDelete,
    alert,
    closeAlert,
    isDeleting,
    isLoading,
  } = useDeleteMovie();

  return (
    <FormWrapper>
      <Typography variant="h5">DELETE MOVIE</Typography>

      {alert && (
        <Alert severity={alert.type} onClose={closeAlert}>
          {alert.message}
        </Alert>
      )}

      <SearchBar
        placeholder="Search movie..."
        value={searchPhrase}
        onChange={e => handleSearchChange(e.target.value)}
      />

      <MovieList>
        {isLoading ? (
          <Typography>Loading...</Typography>
        ) : (
          movies.map(movie => (
            <MovieItem key={movie.movie_id}>
              <Typography>{movie.movie_name}</Typography>
              <IconButton onClick={() => openDeleteModal(movie)}>
                <TrashBin />
              </IconButton>
            </MovieItem>
          ))
        )}
      </MovieList>

      <Modal open={!!movieToDelete} onClose={cancelDelete}>
        <ModalBox>
          <Typography>
            Are you sure you want to delete{' '}
            <strong>{movieToDelete?.movie_name}</strong>?
          </Typography>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <Button
              color="error"
              variant="contained"
              onClick={confirmDelete}
              disabled={isDeleting}
            >
              DELETE
            </Button>
            <Button variant="outlined" onClick={cancelDelete}>
              CANCEL
            </Button>
          </div>
        </ModalBox>
      </Modal>
    </FormWrapper>
  );
};
