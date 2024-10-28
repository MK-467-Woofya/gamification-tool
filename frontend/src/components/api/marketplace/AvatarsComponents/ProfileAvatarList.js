import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

import { ProfileAvatar } from "./ProfileAvatar";

/**
 * Component of list of ProfileAvatars
 * For use with Profile Page
 */
export const ProfileAvatarList = ({ user, avatars, setUser }) => {

    return (
        <Container>
            <Row>
                <h1>Avatars</h1>
            </Row>
            <Row>
                <>
                    {avatars.map(avatar => (
                        <ProfileAvatar key={avatar.id} user={user} avatar={avatar} setUser={setUser}/>
                    ))}
                </>
            </Row>
        </Container>
      );
}