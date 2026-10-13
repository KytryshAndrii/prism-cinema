import React from 'react';
import { Dialog, DialogContent, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { ModalBox, ModalTitle, ModalSubtitle, MoviesGrid, MovieChip } from './styles';
import type { tEntityResponse } from '../../../types/authTypes';
import { useDispatch } from 'react-redux';
import { setFilm } from '../../../store/filmSlice';

type tEntityModalProps = {
  open: boolean;
  onClose: () => void;
  title: string;
  data: tEntityResponse | null;
};

const EntityModal: React.FC<tEntityModalProps> = ({ open, onClose, title, data }) => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  if (!data) return null;

  const handleMovieClick = (movie: any) => {
    dispatch(
      setFilm({
        id: movie.movie_id,
        name: movie.movie_name,
      })
    );

    onClose();
    navigate('/film_entity');
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="sm"
      fullWidth
      PaperProps={{
        sx: { background: 'transparent' },
      }}
    >
      <DialogContent sx={{ p: 0 }}>
        <ModalBox key={title}>
          <ModalTitle>{title}</ModalTitle>

          {data.birthplace && <ModalSubtitle>{data.birthplace}</ModalSubtitle>}

          {data.description && <Typography mb={2}>{data.description}</Typography>}

          <MoviesGrid>
            {data.movies.map(movie => (
              <MovieChip key={movie.movie_id} onClick={() => handleMovieClick(movie)}>
                {movie.movie_name}
              </MovieChip>
            ))}
          </MoviesGrid>
        </ModalBox>
      </DialogContent>
    </Dialog>
  );
};

export default EntityModal;
