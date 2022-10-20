// state storage
import { configureStore, createSlice } from "@reduxjs/toolkit";

let user = createSlice({
  name: "user",
  initialState: "kim",
  reducers: {
    changeName(state) {
      return 'john' + state
    }
  }
});

export default configureStore({
  reducer: {
    user: user.reducer,
  },
});

export let { changeName } = user.actions
