import { useState } from 'react';
import { useAddMovieMutation } from '../../../api/authApi';

type AlertState = { type: 'success' | 'error'; message: string } | null;

const fileToBase64 = (file: File): Promise<string> =>
  new Promise((res, rej) => {
    const reader = new FileReader();
    reader.onload = () => res(reader.result as string);
    reader.onerror = rej;
    reader.readAsDataURL(file);
  });

export const useAddMovie = () => {
  const [form, setForm] = useState({
    title: '',
    rating: '',
    year: '',
    pg: '',
    language: '',
    licence: '',
    trailer: '',
    description: '',
  });

  const [actorIds, setActorIds] = useState<string[]>([]);
  const [directorIds, setDirectorIds] = useState<string[]>([]);
  const [genreIds, setGenreIds] = useState<string[]>([]);

  const [poster, setPoster] = useState<File | null>(null);
  const [previewPoster, setPreviewPoster] = useState<File | null>(null);
  const [subtitles, setSubtitles] = useState<File | null>(null);

  const [alert, setAlert] = useState<AlertState>(null);

  const [addMovie, { isLoading }] = useAddMovieMutation();

  const handleChange = (key: string, value: string) => {
    if (key === 'language') {
      value = value.toUpperCase().slice(0, 3);
    }
    setForm(prev => ({ ...prev, [key]: value }));
  };

  const saveMovie = async () => {
    if (
      Object.values(form).some(v => !v) ||
      !poster ||
      !previewPoster ||
      !subtitles ||
      !actorIds.length ||
      !directorIds.length ||
      !genreIds.length
    ) {
      setAlert({ type: 'error', message: 'Fill all fields' });
      return;
    }

    try {
      const payload = {
        movie_name: form.title,
        movie_rating: Number(form.rating),
        movie_release_date: form.year,
        movie_pg: form.pg,
        movie_description: form.description,
        actor_ids: actorIds.join(';'),
        director_ids: directorIds.join(';'),
        genre_ids: genreIds.join(';'),
        movie_poster: await fileToBase64(poster),
        movie_preview_poster: await fileToBase64(previewPoster),
        movie_trailer: form.trailer,
        movie_language: form.language,
        movie_subtitles_language: form.language,
        movie_subtitles: JSON.parse(await subtitles.text()),
        license_id: form.licence,
      };

      await addMovie(payload).unwrap();
      setAlert({ type: 'success', message: 'Movie created successfully' });
      resetForm();
    } catch {
      setAlert({ type: 'error', message: 'Server error' });
    }
  };

  const resetForm = () => {
    setForm({ title: '', rating: '', year: '', pg: '', language: '', licence: '', trailer: '', description: '' });
    setActorIds([]);
    setDirectorIds([]);
    setGenreIds([]);
    setPoster(null);
    setPreviewPoster(null);
    setSubtitles(null);
  };

  return {
    form,
    handleChange,
    actorIds,
    setActorIds,
    directorIds,
    setDirectorIds,
    genreIds,
    setGenreIds,
    setPoster,
    setPreviewPoster,
    setSubtitles,
    saveMovie,
    alert,
    closeAlert: () => setAlert(null),
    isLoading,
  };
};