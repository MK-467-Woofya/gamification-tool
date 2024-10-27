import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { RefundButton } from "./RefundButton";

/**
 * Single Title display component.
 * For use with the Profile page
 */
export const ProfileTitle = ({ user, title, setUser }) => {
    const uid = sessionStorage.getItem('uid');

    return (
        <Container>   
            <Row className="align-items-center">
                <Col>
                    <h2>{title.text}</h2>
                    <p>Partner: {title.partner}</p>
                </Col>
                <Col>
                    <p>Description: {title.description}</p>
                </Col>
                <Col>
                    <p>Refund {title.name}:</p>
                    <RefundButton user={user} title={title} setUser={setUser}/>
                </Col>
            </Row>
        </Container>
    );
};
