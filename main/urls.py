from django.urls import path
from main.views import (MainView, SportView, MoviesSeriesView, ShowsChannelsView, LiveSearchView, FilterView,
                        FilterPopupsView, FilterResultsView, MovieDetailView, SerieDetailView, ShowDetailView,
                        SportDetailView, ChannelDetailView, ChannelProviderListView, CompilationsListView,
                        MovieCompilationListView, SerieCompilationListView, SportCompilationListView,
                        ShowCompilationListView,
                        ProfileView, RegisterView, RegisterFormView, CodeVerificationView, ProfileCreationView,
                        LogoutUserView, LoginView, LoginFormView,
                        MovieAddToWatchlist, SerieAddToWatchlist, ShowAddToWatchlist, RemoveFromWatchList,
                        ChannelAddToWatchlist,
                        RemoveFromHistoryList, RemoveAccountFromVerification, SettingsView, SubcriptionView,
                        SendFeedbackView, TermsOfUseView, PrivacyPolicyView, FirstTimeScreenView,
                        ModeChangeView, SendComment, LikeComment, ModeChangePostView, SetRating, GetNewRating,
                        PhoneRecoverPassView, PassRecoveryPost, EmailRecoverPassView, changeLocaleView, downloadAppView,
                        workInProgressView,
                        getBonusView, buy2View, buy1View, ChannelCompilationListView, MinusAdf, createShareUrl,
                        addDownload, GetPopup, SendRating
                        )

urlpatterns = [
    path('', MainView.as_view(), name="main_page"),
    path('mode-change-post', ModeChangePostView.as_view(), name="mode-change-post-page"),
    path('sports', SportView.as_view(), name="sports_page"),
    path('movies-series', MoviesSeriesView.as_view(), name="movies-series_page"),
    path('shows-channels', ShowsChannelsView.as_view(), name="shows-channels_page"),
    path('live-search.json', LiveSearchView.as_view(), name="live-search-post"),
    path('filter', FilterView.as_view(), name="filter-page"),
    path('filter.json', FilterPopupsView.as_view(), name="filter-popups-post"),
    path('filter-results', FilterResultsView.as_view(), name="filter-results"),

    path('movie/<int:pk>', MovieDetailView.as_view(), name="movie-page"),
    path('serie/<int:pk>', SerieDetailView.as_view(), name="serie-page"),
    path('tv-show/<int:pk>', ShowDetailView.as_view(), name="show-page"),
    path('sport/<int:pk>', SportDetailView.as_view(), name="sport-page"),
    path('channel/<int:pk>', ChannelDetailView.as_view(), name="channel-page"),

    path('movie-list/<int:pk>', MovieCompilationListView.as_view(), name="movie-list-page"),
    path('serie-list/<int:pk>', SerieCompilationListView.as_view(), name="serie-list-page"),
    path('sport-list/<int:pk>', SportCompilationListView.as_view(), name="sport-list-page"),
    path('show-list/<int:pk>', ShowCompilationListView.as_view(), name="show-list-page"),
    path('channel-list/<int:pk>', ChannelCompilationListView.as_view(), name="channel-list-page"),

    path('provider/<int:pk>', ChannelProviderListView.as_view(), name="provider-page"),
    path('compilations/<int:pk>', CompilationsListView.as_view(), name="compilations-list-page"),

    path('first-time-screen', FirstTimeScreenView.as_view(), name="first-time-page"),
    path('mode-change', ModeChangeView.as_view(), name="mode-change-page"),

    path('profile', ProfileView.as_view(), name="profile-page"),
    path('register', RegisterView.as_view(), name="register-page"),
    path('register/form', RegisterFormView.as_view(), name="register-form-page"),
    path('code-verification', CodeVerificationView.as_view(), name="register-code-verificarion"),
    path('remove-from-verivication', RemoveAccountFromVerification.as_view(), name="remove-from-verificarion"),
    path('recover-phone', PhoneRecoverPassView.as_view(), name="recover-phone"),
    path('recover-email', EmailRecoverPassView.as_view(), name="recover-email"),
    path('pass-recovery-post', PassRecoveryPost.as_view(), name="pass-recovery-post"),

    path('profile-creation', ProfileCreationView.as_view(), name="profile-creation"),
    path('logout', LogoutUserView.as_view(), name="user-logout"),
    path('login', LoginView.as_view(), name="login-page"),
    path('login/form', LoginFormView.as_view(), name="login-form-page"),
    path('feedback', SendFeedbackView.as_view(), name="feedback-page"),
    path('settings', SettingsView.as_view(), name="settings-page"),
    path('subscription', SubcriptionView.as_view(), name="subscription-page"),
    path('language', changeLocaleView.as_view(), name="locale-page"),
    path('app-download', downloadAppView.as_view(), name="app-download-page"),
    path('work-in-progress', workInProgressView.as_view(), name="work-in-progress-page"),
    path('get-bonus', getBonusView.as_view(), name="get-bonus-page"),

    # watch-list
    path('movie/<int:pk>/add-to-watchlist', MovieAddToWatchlist.as_view(), name="movie-add-to-watchlist"),
    path('serie/<int:pk>/add-to-watchlist', SerieAddToWatchlist.as_view(), name="serie-add-to-watchlist"),
    path('tv-show/<int:pk>/add-to-watchlist', ShowAddToWatchlist.as_view(), name="show-add-to-watchlist"),
    path('channel/<int:pk>/add-to-watchlist', ChannelAddToWatchlist.as_view(), name="channel-add-to-watchlist"),
    path('remove-from-wl', RemoveFromWatchList.as_view(), name="remove-from-watchlist"),
    path('remove-from-hl', RemoveFromHistoryList.as_view(), name="remove-from-historylist"),

    # rules
    path('privacy-policy', PrivacyPolicyView.as_view(), name="privacy-policy-page"),
    path('terms-of-use', TermsOfUseView.as_view(), name="terms-of-use-page"),

    # comments
    path('sendcomment', SendComment.as_view(), name="send-comment"),
    path('likecomment', LikeComment.as_view(), name="like-comment"),

    # rating
    path('setrating', SetRating.as_view(), name="set-rating"),
    path('getrating', GetNewRating.as_view(), name="get-rating"),
    path('minus-adf', MinusAdf.as_view(), name="minus_adf"),
    path('createShareUrl', createShareUrl.as_view(), name="create_share_url"),
    path('add_download', addDownload.as_view(), name="add_download_url"),

    path('buy1sub', buy1View.as_view(), name="buy1"),
    path('buy2sub', buy2View.as_view(), name="buy2"),

    # Popup-Manager
    path('get-pp', GetPopup.as_view(), name="get-pp"),
    path('send-rating', SendRating.as_view(), name="send-rating"),

]
