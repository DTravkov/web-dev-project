
import { JwtPayload } from "jwt-decode";
export interface ITokenDecoded extends JwtPayload {
    user_id: string
    is_manager: boolean
}