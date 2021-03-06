'use strict';

var React = require('react');

var modalActionCreators = require('../action-creators/modal-action-creators');
var platformManagerActionCreators = require('../action-creators/platform-manager-action-creators');
var platformRegistrationStore = require('../stores/platform-registration-store');

var RegisterPlatformForm = React.createClass({
    getInitialState: function () {
        return getStateFromStores(this);
    },
    componentDidMount: function () {
        platformRegistrationStore.addChangeListener(this._onStoresChange);
    },
    componentWillUnmount: function () {
        platformRegistrationStore.removeChangeListener(this._onStoresChange);
    },
    _onStoresChange: function () {
        this.setState(getStateFromStores());
    },
    _onCancelClick: modalActionCreators.closeModal,
    _onSubmit: function () {
        platformManagerActionCreators.deregisterPlatform(this.props.platform);
    },
    render: function () {
        return (
            <form className="register-platform-form" onSubmit={this._onSubmit}>
                <h1>Deregister platform</h1>
                <p>
                    Deregister <strong>{this.props.platform.name}</strong>?
                </p>
                <div className="form__actions">
                    <button
                        className="button button--secondary"
                        type="button"
                        onClick={this._onCancelClick}
                        autoFocus
                    >
                        Cancel
                    </button>
                    <button className="button">Deregister</button>
                </div>
            </form>
        );
    },
});

function getStateFromStores() {
    return { error: platformRegistrationStore.getLastDeregisterError() };
}

module.exports = RegisterPlatformForm;
