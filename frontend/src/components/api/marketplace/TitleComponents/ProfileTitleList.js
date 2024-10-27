import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

import { ProfileTitle } from "./ProfileTitle";

/**
 * Component of list of ProfileTitles
 * For use with Profile Page
 */
export const ProfileTitleList = ({ user, titles, setUser }) => {

    return (
        <Container>
            <Row>
                <h1>Titles</h1>
            </Row>
            <Row>
                <>
                    {titles.map(title => (
                        <ProfileTitle key={title.id} user={user} title={title} setUser={setUser}/>
                    ))}
                </>
            </Row>
        </Container>
      );
}