from decision_transformer.models.decision_transformer import DecisionTransformer

#teste
state_dim = 11
act_dim = 3
max_length = 20
max_ep_len = 1000
hidden_size = 128
n_layer = 3
n_head = 1
n_inner = 4*hidden_size
act_func = 'relu'
n_positions = 1024
dropout = 0.1

model = DecisionTransformer(
    state_dim = state_dim,
    act_dim = act_dim,
    max_length = max_length,
    max_ep_len = max_ep_len,
    hidden_size = hidden_size,
    n_layer = n_layer,
    n_head = n_head,
    n_inner = n_inner,
    activation_function = act_func,
    n_positions = n_positions,
    resid_pdrop = dropout,
    attn_pdrop = dropout,
)

#n testado
warmup_steps = variant['warmup_steps']
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=variant['learning_rate'],
    weight_decay=variant['weight_decay'],
)
