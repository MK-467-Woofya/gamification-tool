import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

import { ShopTitle } from "./ShopTitle";

/**
 * Component of list of ProfileTitles
 * For use with the Title Page
 */
export const ShopTitleList = ({ user, titles, setUser }) => {

    return (
        <Container>
            <Row>
                <h1>Titles</h1>
            </Row>
            <Row>
                <>
                    {titles.map(title => (
                        <ShopTitle key={title.id} user={user} title={title} setUser={setUser}/>
                    ))}
                </>
            </Row>
        </Container>
      );
}