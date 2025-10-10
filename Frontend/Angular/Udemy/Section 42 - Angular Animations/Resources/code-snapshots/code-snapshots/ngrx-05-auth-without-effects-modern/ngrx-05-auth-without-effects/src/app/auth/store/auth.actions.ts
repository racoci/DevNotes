import { Action } from '@ngrx/store';

export const LOGIN = 'LOGIN';
export const LOGOUT = 'LOGOUT';

export class Login implements Action {
  readonly type = LOGIN;

  constructor(
    public payload: {
      email: string;
      userId: string;
      token: string;
      expirationDate: Date;
    }
  ) {}
}

export class Logout implements Action {
  readonly type = LOGOUT;
}

export type AuthActions = Login | Logout;

// Alternative syntax:
// import { createAction, props } from '@ngrx/store';

// export const login = createAction(
//   '[Auth] Login',
//   props<{
//     email: string;
//     userId: string;
//     token: string;
//     expirationDate: Date;
//   }>()
// );

// export const logout = createAction('[Auth] Logout');
