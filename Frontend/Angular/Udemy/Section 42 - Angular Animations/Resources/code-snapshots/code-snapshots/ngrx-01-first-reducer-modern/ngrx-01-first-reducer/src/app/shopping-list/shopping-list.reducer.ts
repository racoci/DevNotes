import { Action } from '@ngrx/store';

import { Ingredient } from '../shared/ingredient.model';

const initialState = {
  ingredients: [
    new Ingredient('Apples', 5),
    new Ingredient('Tomatoes', 10),
  ]
};

export function shoppingListReducer(state = initialState, action: Action) {
  switch (action.type) {
    case 'ADD_INGREDIENT':
      return {
        ...state,
        ingredients: [...state.ingredients, action]
      };
  }
}

// Alternative syntax:
// Using recent NgRx features (e.g., createReducer() and on()).

// import { createReducer, on } from '@ngrx/store';

// import { Ingredient } from '../shared/ingredient.model';
// import * as ShoppingListActions from './shopping-list.actions';
//
// export interface State {
//   ingredients: Ingredient[];
//   editedIngredient: Ingredient;
//   editedIngredientIndex: number;
// }
//
// const initialState: State = {
//   ingredients: [
//     new Ingredient('Apples', 5),
//     new Ingredient('Tomatoes', 10),
//   ],
//   editedIngredient: null,
//   editedIngredientIndex: -1
// };
//

// Below code will not work yet, since we have not yet created the shopping list actions.
// But we can still see how the reducer will work (soon)
// export const shoppingListReducer = createReducer(
//   initialState,
//   on('ADD_INGREDIENT', (state, action) => ({
//     ...state,
//     ingredients: [...state.ingredients, action.ingredient]
//   })),
// );
