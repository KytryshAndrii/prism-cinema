import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { useDebounce } from '../../../hooks/useDebounce';
import { useSearchMoviesQuery } from '../../../api/authApi';
import { setFilm } from '../../../store/filmSlice';
import { SearchInput } from '../styles';
import { SearchResultItem, SearchResults, SearchWrapper } from './styles';
import type { tMovieResponse } from '../../../types/authTypes';

const SearchBar: React.FC = () => {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const debouncedQuery = useDebounce(query, 150);
  const { data } = useSearchMoviesQuery(debouncedQuery, {
    skip: debouncedQuery.trim() === '',
  });

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleClick = (film: tMovieResponse) => {
    dispatch(
      setFilm({
        id: film.movie_id,
        name: film.movie_name,
      })
    );
    setQuery('');
    setIsFocused(false);
    navigate('/film_entity');
  };

  const handleBlur = () => {
    setTimeout(() => setIsFocused(false), 150);
  };

  return (
    <SearchWrapper>
      <SearchInput
        ref={inputRef}
        type="text"
        placeholder="Search..."
        value={query}
        onChange={e => setQuery(e.target.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={handleBlur}
      />
      {isFocused && query.trim() !== '' && data && data.length > 0 && (
        <SearchResults>
          {data.map(film => (
            <SearchResultItem key={film.movie_id} onClick={() => handleClick(film)}>
              {film.movie_name}
            </SearchResultItem>
          ))}
        </SearchResults>
      )}
    </SearchWrapper>
  );
};

export default SearchBar;
