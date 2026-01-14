import { createSlice, type PayloadAction } from "@reduxjs/toolkit"

type tFilmState = {
    id: string | null;
    name: string | null;
    poster: string | null;
    preview_poster: string | null;
};

const initialState: tFilmState = {
    id: null,
    name: null,
    poster: null,
    preview_poster: null,
};

const filmSlice = createSlice({
    name: "film",
    initialState,
    reducers: {
        setFilm: (_, action: PayloadAction<tFilmState>) => {
            return { ...action.payload };
        },
        clearFilm: () => initialState,
    },
});


export const { setFilm, clearFilm } = filmSlice.actions;
export default filmSlice.reducer;