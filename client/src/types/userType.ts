export type UserSignup = {
    login: string,
    secret_string: string
}

export type UserSignin = {
    login: string,
    secret_string: string,
    expiration: string,
    code: string
}