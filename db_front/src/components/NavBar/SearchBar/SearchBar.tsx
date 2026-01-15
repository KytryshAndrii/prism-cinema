import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useDebounce } from "../../../hooks/useDebounce";
import { useSearchMoviesQuery } from "../../../api/authApi";
import { setFilm } from "../../../store/filmSlice";
import { SearchResultItem, SearchResults, SearchWrapper } from "./styles";
import { SearchInput } from "../styles";


const SearchBar: React.FC = () => {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebounce(query, 300);
  const { data, isLoading, isError } = useSearchMoviesQuery(debouncedQuery, {
    skip: debouncedQuery.length === 0,
  });

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleClick = (film: { id: string; name: string }) => {
    dispatch(setFilm({
      id: film.id,
      name: film.name,
      poster: null,
      preview_poster: null,
    }));
    setQuery("");
    navigate("/film_entity");
  };

  return (
    <SearchWrapper>
      <SearchInput
        type="text"
        placeholder="Search..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      {data && data.length > 0 && (
        <SearchResults>
          {data.map((film) => (
            <SearchResultItem key={film.id} onClick={() => handleClick(film)}>
              {film.name}
            </SearchResultItem>
          ))}
        </SearchResults>
      )}
    </SearchWrapper>
  );
};

export default SearchBar;
