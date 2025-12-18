use sekha_controller::storage::db::{init_db, DbPool};
use sqlx::sqlite::SqlitePoolOptions;
use std::sync::Arc;
use tokio::sync::RwLock;
use sekha_controller::config::Config;
use sekha_controller::api::routes::AppState;
use sekha_controller::storage::repository::Repository;

pub async fn setup_test_app() -> (AppState, DbPool) {
    // Use in-memory database for tests
    let pool = SqlitePoolOptions::new()
        .connect("sqlite::memory:")
        .await
        .expect("Failed to create test database pool");
    
    init_db(&pool).await.expect("Failed to initialize test database");
    
    let config = Arc::new(RwLock::new(Config::default()));
    let repo = Repository::new(pool.clone());
    
    let state = AppState {
        config,
        repo: Arc::new(repo),
    };
    
    (state, pool)
}