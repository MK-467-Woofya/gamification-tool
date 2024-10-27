import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

import { ShopAvatar } from "./ShopAvatar";

/**
 * Component of list of ProfileAvatars
 * For use with the Avatar Page
 */
export const ShopAvatarList = ({ user, avatars, setUser }) => {

    return (
        <Container>
            <Row>
                <h1>Avatars</h1>
            </Row>
            <Row>
                <>
                    {avatars.map(avatar => (
                        <ShopAvatar key={avatar.id} user={user} avatar={avatar} setUser={setUser}/>
                    ))}
                </>
            </Row>
        </Container>
      );
}