import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { RefundButton } from "./RefundButton";

/**
 * Single Avatar display component.
 * For use with the Profile page
 */
export const ProfileAvatar = ({ user, avatar, setUser }) => {
    const uid = sessionStorage.getItem('uid');

    return (
        <Container>   
            <Row className="align-items-center">
                <Col>
                    <img src={avatar.img_url} alt={avatar.name} width={100} height={100}/>
                </Col>
                <Col>
                    <h2>{avatar.name}</h2>
                    <p>Partner: {avatar.partner}</p>
                </Col>
                <Col>
                    <p>Description: {avatar.description}</p>
                </Col>
                <Col>
                    <p>Refund {avatar.name}:</p>
                    <RefundButton user={user} avatar={avatar} setUser={setUser}/>
                </Col>
            </Row>
        </Container>
    );
};
